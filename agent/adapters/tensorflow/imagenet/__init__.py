#
# adapters/tensorflow/imagenet/__init__.py - a service adapter for the tensorflow ImageNet pre-trained graph
#
# Copyright (c) 2017 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

import base64
import logging
import os
from pathlib import Path
from typing import List

import tensorflow as tf

from adapters.tensorflow.imagenet.node_lookup import NodeLookup
from sn_agent.job.job_descriptor import JobDescriptor
from sn_agent.ontology import Service
from sn_agent.service_adapter import ServiceManager, ServiceAdapterABC

IMAGENET_CLASSIFIER_ID = 'deadbeef-aaaa-bbbb-cccc-111111111102'

logger = logging.getLogger(__name__)

FLAGS = None

AGENT_DIRECTORY = Path(__file__).parent

CHECK_ACCURACY = False

MINIMUM_SCORE = 0.20


class TensorflowImageNet(ServiceAdapterABC):
    type_name = "TensorflowImageNet"

    def __init__(self, app, service: Service, required_services: List[Service] = None):
        super().__init__(app, service, required_services)
        if not service.node_id == IMAGENET_CLASSIFIER_ID:
            raise RuntimeError("TensorflowImageNet cannot perform service %s", service.node_id)

    def example_job(self):
        bucket_image_64 = '/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxAQEBUQEhAQFRUQEg8SEA8VEBUQFRAPFRUWFhUVFRUYHSggGBolGxUVITEhJSkr' \
                          + 'Li4uFx8zODMtNygtLisBCgoKDg0OFxAQGi0lHR0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t' \
                          + 'LS0tLf/AABEIAOEA4QMBEQACEQEDEQH/xAAbAAEAAgMBAQAAAAAAAAAAAAAAAgMBBQYEB//EAEEQAAIBAgIHBAgEBAMJAAAAAAAB' \
                          + 'AgMRBCEFBhIxQVFhInGBkRMyUmKhscHRFEJykkOC4fAHU/EVFhcjM1RjotL/xAAaAQEBAQEBAQEAAAAAAAAAAAAAAQIDBQQG/8QA' \
                          + 'LBEBAQABAwMEAQMDBQAAAAAAAAECAwQREiExBRNBUSIyYaEVcZEjUoGx8P/aAAwDAQACEQMRAD8A+4gAAAAAAAAAAAAAAAAAAAAA' \
                          + 'AAAAAAAAAAAAAAAAAAAAAAAGGwK54iC3zgu+SQZuUnyqlpGgt9an++P3Ce5h9xB6Xw6/jU/3Icp72n9xH/bOG/zqfmOU97T+4ktL' \
                          + 'Yd/xqf7kOV97D7iyOPovdVp/vQX3MftdGtF7pRfc0w1zEwoAAAAAAAAAAAAAAAAAGB4cTpahT9apG/Jdp/AcuWWthj5rUYvXGhD1' \
                          + 'Yyl1bUUTl8+e+wx8NHjNfJ7o7Ee5bT+Ji6kj5M/Uvpp8RrhiJfxZ+D2fkZurHy5eoZ35a+tpytPfOT75NmLquN3Wd+Xnljqj4k9y' \
                          + 'se7lUPxM+bJ11OvI9NLmx106qyq0uZeunVU44qfTyLNStddWLGy5R8mX3KvuVNaSa/L5SaNTUX37HqpadnHdOqu6dy+5HWbrKfNb' \
                          + 'DDa211urS/njf7l647Y7/P7bWhrtUXrRpyXFrJ/34GuX0Y+oWeY22E1woT9aMo9cpL7l5fRhvtPLy3GF0pQq+pUi3yvZ+TK+nHVw' \
                          + 'y8V7A6AAAAAAAAACutWjCLlKSilvbdglsk5rntJa1Rjf0aT9+WS8FvZOXx6m8k/S43S+tk5ZObl03R8kc8tSR5etv7e3LncRpepP' \
                          + 'jZHK6tvh5+e5zyeV1JPe2c7bXHqt81mMQ1IsiiNyJpBuRJIKzYqslVkDJRkDDRSwsE4EgSAVJTZeqi+li5R4m5m3jqWN5ozWatTy' \
                          + 'VR29mXaXk/odJlK+zS3mePy6zR2tlOeVWOy/bXaj4rejXL0dPeY5fqdDSqRklKLTT3NO6ZX1yy94mFAAAAB4tK6Rhh4bUs2/Vjxk' \
                          + '/sHPV1ZpzmuC0zpac71Kksluj+WPcjNvDyNfXt/LKuN0hpOVR5OyPmz1LfDydTWyz/s8KObinFERZFBqRZFB0iaDcSRVZQVkqpAZ' \
                          + 'KoBkoACgACAAAB6cNinF2e7mdMc/tvDPh0miNLVKDvB3i/Wpt5SXTk+p1eho6+WHjw77AYyFamqkHk+HGL4p9TT1sM5nOY9IbAAA' \
                          + 'DgNN4x1a0pcItxiuUVkZeTr59WdcbrLXe0ocErvx3HDWvw8nd5flMWlSOD5OVkYkE0inCaDcTQbiSDSSCsoqshWSjIVlFADJQAAA' \
                          + 'AAoBGANto6V4dzt4HfC9n06V5xdVqXi3GtKlwnFyt70ePk/gbj0dln+VxdqV6QAAwwPmld9uX6n8zLxc/wBVaHWLCOVqqz2Vsz7u' \
                          + 'DOOrjz3fBu9Pn840iifM+LhJILwykGuEkF4SQaSTCs3Cs3KMoKyVWbgCjJVZuAAFAIBWQAGYQcnZK7e5Fk5JLe0bmhS2IqPLe+b4' \
                          + 'n0YziPqxnTOG31OntY1JflhUb8rfUsvd9uynOdr6GaeoAAAHz3WvASoVnNLsVM4vk+MSeHj7zTuGfVPFamlXUvqh5fNMpWuxmiE8' \
                          + '6dl7j3fyv6Hz56PPeOGe3+cf8NVUpOLtJNPk1Y+e42eXzXGztUSIAZuFZuFLgSTKrNwrNyqzcDJeVZuUAMlAAAuBko9NHBSlv7K6' \
                          + '7/I3MLXTHTte6nCFNcube9naSYusmOEavHaYTexTzu7bS+S5kuXPhjrud4xfSNQ9Ayw1L0tVWqVUuy98Ib7Pq978DWM4e5tdH28O' \
                          + '7qjT6gAAApxeGhVg6c4qUZb0/wC8mGc8JlOK+eaf1Vq4dupSvUp78vXguq4rqjnZZ4eLuNlnp/lh3jS0cY1vLMvt8uOpXpvGas0p' \
                          + 'Lz/0LZK6czKd3kq6JhL1W49PWXxzOWWjjfDnlt8b4eKromot2zLudvgzldDKeHHLQyjy1MPOO+El4HO4ZTzHO45TzFW0ZY5EwvLK' \
                          + 'YXlJMKkmGmUUZKrJRkBcqrIUpPdF+RqY2rxaujgpvku9m5p5NTCr4YCK9aXgsjc0p8tTTnzU51qNL2V14/c1+OK9WGLWYzWOK9RN' \
                          + '9dyMXV+mbq2+I8GDo4vSFRUqcXLaf6YR6tmPyya09DPVvEfVtUNRaWCtVqtVay3St2Kb9xPj1fwO+OPD2dts8dLve9dgbfaAAAAA' \
                          + 'Bhq+QHznTujYbcuzZpvNZXMWPJ3Whjzzw0FTDOLyf0Jw864WeF2D9NUqRpRW1KbtFO2fiWWtYdeWUxnmul/3XxKhtP0V0rumpv5t' \
                          + 'WNd3oTZanHPZop4iKbjJ7Mou0oyi04vk7GeY+TLKS8XtUJOnLe6T77fVDtWfxv0rlg6T/hx8GvoydGN+Gbp4X4QejqXsyXc2S6WH' \
                          + '0ntYfSD0bS9/zZn2cE9rBB4Cnzl5/wBB7OKe3ix+Dpe1Lz/oPaxTow+2fw9Dm/Me3gvTgbGHX+rL06cT/THXw8eEfmPwh16cQlpW' \
                          + 'jHdbwRfcxie/hPDz1dPxW5Nmbqxn378R4q2sEuCS78zN1anuZ14aukq89zfgrE6sqcW+arhhJzzlJLx2n8CdNaxwjY4HRlNO7W1+' \
                          + 'rd5I1MY+jTwj6XqHhO05WSUI2StazfLwud8Y9jbY8R2xp9QAAAAAAAByms1Dtt81czXybnHlyWKgHlZx7dUpxjio34xmovlJoR12' \
                          + 'Vk1py7v0hp7jgdddF1FV/FRjeEk4VWt8WvVk1y4XOWU4vLyPUtC3jUx/5cVV0nTU3G0nsuzkkmr9M8znbHk3BNY+m+L8mZ6oxeyf' \
                          + '4te38y9X7s9V+0ZYz3/ix1funVkreNXtrzJz+7POorljF7a8xynGorli17a8yL0ZqpYqPtfML7eSqWJjzfkRqaVQ9OuUvgg3NNly' \
                          + 'V7KL8X9jcxi8RJdy8i8SKupRvnfeWNeXrpQK1G1wUBH1aUfStS7KEo8XsvwzR2j2dGcYulK6gAAAAAAAGl1kpXipcrolcdac4uJx' \
                          + 'sM2R5GpGuldO6bTWafJh895l5jf6L1nltRhWtZ5elW9Pg5fcSvQ0N/eZjqf5dWlFx2Wk4yWaeakmbep2sfK9dtVPwsvS0l/ypPL/' \
                          + 'AMbfB/RnzamHDwt9tbpXrx/Tf4crFWODzbeXogWOVZcCpMlM6Rmx0map0yNzJBwDXKLiVeWNkcrynShdmse9S1ZTjmdWeV+zcWKu' \
                          + 'oQaQxnZqPZCJXad22wECx9ejHdatVLVUuacfhf6HSeXr4eHWmmwAAAAAAADx6Xp7VKXTMVnOcxwWOhmZeTqzu1NVB8mTzzRHKt/q' \
                          + '3p30dqNV9jdCb/I+T6fIsr0NnvOn8M/DrqtONSLpzSlGSs4vNNM3e717JlOL4r5ZrZqxLCS24XlRk+zLe4P2ZfRny6mnw/Ob3ZXQ' \
                          + 'vVj+m/w51HJ59WRYjFjNioqnAljcqqUTLpKg0GpUWiryspqyOuMS1ZSiWEWRWaJle8bxeqKOjT10Vcjtj3brRsc78s/I1i9DRjpN' \
                          + 'AVO3CXvr4v8AqXGvR0/Dujo2AAAAAAAARqw2otc00BwGk6dm+hl5evj3aWsg+HJ5ZkcqpkiMV0eren9m1Gs+zup1G/V92T5dTUye' \
                          + 'ls95x+Gfj4rqa0Yzi4TSlGSs4vNNGr3evZMpxfD5xrTqrLDt1aV5Ut7W+VLv5rqfNnp8d4/P730+6f56ffH/AKcucXlpKReU4ZNI' \
                          + 'rnEzY3KqaI2wo3yEnKrZRtY7xEopIvDUTptN9UZuPLeL0QefmbbnPL24ZB3wjpNB4dTlsvds1JS/TGLb+hqPS0I2eiE1GHfH5oYe' \
                          + 'H26c7O/OjYAAAAAAAAA43WCjapJdb+eZmvh3OLmcQg83J46gcclMjLnVTDLf6C1gdO1Ks24boz3uHR818izJ6O033R+Gp4+3Vqom' \
                          + 'uDTW/emmbe3LLOzkNY9UFO9XDJJ75Udyf6OT6HHPT+Y8nd+mzLnPS8/ThatOUW4yTTi7OLVmn1R89nDw8sbjeL5RUhyzwncqcITj' \
                          + 'yHDUqdKnbM3jjw0lNXRpVdN8GaIzh09pkbx8vXDj3FdI2OFW4Pr046LRTtRrz5whRj+qpLP/ANYsvPavQ0vFbnA07OCW/aj80akf' \
                          + 'bjOI7c2oAAAAAAAAA53Welmpc1byJXz7idnG4qJHk5x4agcMlEiVzqqRlmq2GWx0RpueH7L7VPjDjHrF8O4sy4fVtt7lo9r3x/8A' \
                          + 'eHX4TGwqx26crrjwcXya4M3Ly9/S1sNXHqwrx6Y0PQxS7atNerVjlJd/NGcsJk57ja6evPynf7cFprV2vhrtrbhwqxzVveX5T58s' \
                          + 'Li8HcbHU0e/mfbUJmI+PhJ3NeGWVOxZViamjcrcqFWPFGotidGpffv8AmWxrHJ6oR3+BHaYvbTqpfcza+rGyOj1cTqUllaPpJz/U' \
                          + '7KMX3JJ+bNYd3o7Wc48us0NQ2qyfCF5Pv3L++h1j7XTFQAAAAAAAAAavWGlelf2X8H/aJXPVnOLhcZEjyNSNbUQfNk88kRyqqSIz' \
                          + 'VciM1XIjFZw2KqUpbcJOL+DXJriizsunrZ6WXVheK6fR2sVOpaNS0Jc/ySffwNzLl7u29Swz7Z9r/DcqbXVPxTRXp9q0ukNXMNWb' \
                          + 'lFeim+MV2W+sfsYuE8vh1/T9LU7ztf2c7pDVvEUs9j0kfah2suq3ozca8nW9P1dPxOZ+zR1cO1/8vJnO4/T4rjZ5UNNGfDLO0WZN' \
                          + 'cl0amZ2WxqpL+2Lk6zLjw6PQur1as1OrFwp79lq0p+HBFmNr0tvtM871Z9p9O2pUowiopJJKySO0nD2ZJJxHS6Hwvo6d2u1PN9Fw' \
                          + 'Roe8AAAAAAAAAAox1PapyXuvzWYS+Hz7HQzMvJ1se7VVUHx5PNNEc7FUkRiqpEYquRGaqkg51XJBHrwOlq1HKMrx9iWcfDl4FmVj' \
                          + '69Deauj+m9vqt/hNY6M8pp03z9aPnvRrqj2NH1LTy7Zdr/DbUayktqE1Jc07mnoY545TnG8o4mjTqf8AUpQl1az8ycSs56OGf6py' \
                          + '1tbVvCT3bcPHaXxM3CPkz9N0cvHZ4p6l0nurtfyoz7T576Tj8ZUhqRS415PuSRPaJ6Tj85VtMBq5hKLUlHaks1KT2rPotyNTTkfX' \
                          + 'pbHS07zJ3bb06TUVvbSS4tvodH19o3+i9FbHbqWcuEeEPuyq2oQAAAAAAAAAAAHCaYo7M5Lk2jLztxj3aGsg8/J5ZkcqokRiqZkY' \
                          + 'quQYquRGKrkGVbCosKzTqyi7xk4vmnYOuOeWN/G8NhQ1gxMPzqS96KfxLMq+zDf62Pzz/d7aWtUvzUovuk18y9T6sfU8vnFctaY/' \
                          + '5L/ei9Tr/Up/tRlrM/y0l4y+xOtb6h9YqpaZrTyuor3Vb4vMnVWLutTJvdT6DniYN52bm289y+9jWLvoTm930g2+0AAAAAAAAAAA' \
                          + 'ADldZ6Nql/aSf0M18m4xcniFmHl5PFUI4V55krnVUiMVXIM1CRGKrYRWwItBpFoNRGwWFg3Ekg6RbBEdI9mGiV203fag0O1OfsxU' \
                          + 'fFu/0OmL1NvO3LtDT6QAAAAAAAAAAAANJrNRvCMuV0SuOvOcXEYuOZHkak7tfVQfPk80iOVVMyygwxVciM1BhlWwqLQWItEa+WA0' \
                          + 'FaiaQbi2miOuL3YZFj6dOPp2peH2cNte3JvwWS+TOserozjFvyuoAAAAAAAAAAAAHi0xS2qMuma8CVnOc4uAx0cyPH1p3auqg+TK' \
                          + 'PLMjlVUiMq5EZqEgxVciIgwiLDTFgsYsG4ykGolEjcW00V1xjYYSOZY+vSnd9e0VQ9HQpw9mEb99rv4nV6+M4kj1hQAAAAAAAAAA' \
                          + 'AAI1I3TXNNAfPtK0XGTT4Noy8rcY8VpKyD4co8s0RxqmRGKrkRmq5BmoMjKLC8otBUbBYxYNMoNROKI6RbTQdcY3ur2EdavTppb5' \
                          + 'JvpFZt+SN4vv2+POUfWUdHpsgAAAAAAAAAAAAAAc5rVo5temity7a6e0Svk3OnzOqOIxCI8nJ46hHCqJEYqtkYVsMoMjKDQGGg0i' \
                          + 'GoMNCI1EkHSL6Yd8Y+nakaFdGn6aorTqpWT3wp8F3vf5HXGPX2+n048105p9AAAAAAAAAAAAAAABhoDjtY9W5K9WirrfKmt8esea' \
                          + '6E4ebudrf1Yf4cbVVjLy8o88iOdVyRGKraDKLRGUGgIhYiGoEagkGonTi20km23ZJZtvkkHbCc3iPoeqOqDg1XxKW0s6dF57L4Sn' \
                          + '16cDpjj9vW2+26fyydubfcAAAAAAAAAAAAAAAAAADT6Y1doYntNbM/8AMjx71uZOHza21w1fPlxek9UsTSu4x9JHnDfbrHf5GbHl' \
                          + '6ux1MfHdz1anKLtJNPk1Z+TMvhyxs8qmgxUGiM1BoIjYLGLBqRKlRlN7MYyk+CScm/BEdccMsvEdJonUfFVrOolRjzlnLwivrY1M' \
                          + 'a+/S2GeXfLs7zQerWHwmcI7U+NWWcvD2fA6THh6elt8NPxO7cldwAAAAAAAAAAAAAAAAAAAAACjEYSnUVp04S/VFMM5YY5eY02J1' \
                          + 'Nwc81CUP0zaXk7memPly2Ojl8NfU/wAP6D3Vqq8Iv6Dpcb6Zp/dU/wDDyn/3E/2L7k6Gf6Xh9raX+HuHXrVar7tmP0L0xvH03Tnm' \
                          + '1sMNqZgYb6Tn+ubfwVkOmO2Oy0cfhusLg6VJWp04QXuxUfkafTjhjj4i8NAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' \
                          + 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD//2Q==';

        cup_image_64 = '/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxAPDw0PDQ0PDg0PDQ0PDQ0PDQ8ODQ0NFRIWFhUSExUYHyghGB4lJxMWITEhJSor' \
                       + 'Li4uGB8zODMsNygtLisBCgoKDQ0NDxAPFSsdFRktLSs4LCsrKysrKysrKzcrLSsrKy0tKzcrKysrKysrKystNy0rKysrKysrKysr' \
                       + 'KysrK//AABEIAOEA4QMBIgACEQEDEQH/xAAcAAEAAQUBAQAAAAAAAAAAAAAAAQIDBAUGBwj/xABAEAEAAgECAgcEBAoLAQAAAAAA' \
                       + 'AQIDBBEFIQYHEhMxQWFRcZGxMkKBghQiI3KDkqGissEIF1NUYpOjwtHh8BX/xAAWAQEBAQAAAAAAAAAAAAAAAAAAAQL/xAAWEQEB' \
                       + 'AQAAAAAAAAAAAAAAAAAAEQH/2gAMAwEAAhEDEQA/APcQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' \
                       + 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' \
                       + 'AEJavjHGKabsRe1K3vv2O3aKVnbbfn9scgbRG7jtV0g1XjSKxWfCa0i1fjzYF+OaqfHPMfmxWPkD0Dc3ee//AEs0/SzXn70q6ay0' \
                       + '+N7frSlHf7m7iseaZ+tPxlk4r+s/GVHWG7n8NLz4Tf8AWmGTSuSNvyto+9MiVuBqq58sfW329tYU243XHMRmmkbzFYmLecztHKRW' \
                       + '3EQkAAAAAAAAAAAAAABby56UibXvWlY8bWmKxH2y13SPjWPRae+fJtO3KlZtFe3f2b+UcpmZ8oiXzv0g41rOOavutPGfUT2prWkX' \
                       + 'tGGN5+rjjlWvrbefOdvAH0Nk6T6Cv0tdp4/TUl551q8c0mpppq6fU481/wAtE1pbteVZ5uMp1McVmsTP4LW08+xOptvHpvFWB0g6' \
                       + 'DcQ4Vp41GpjT1xfhGPfusk5LTNpiu2+0bRyhUYmk4jk0/b7jJOObREb18vWPZ4s7F0y1lYiLXrl287d5Fp98xZps/jLGmVSOjv03' \
                       + '1EzMzHYjs8opett7b+M9uszt6Ndbp7xKsztfBNd+W+Cm+3q02SWLkNV0tesjicf3f/Jj/lcjrO4p7dNH6H/tyMoQdl/Wjxfy1GGv' \
                       + 'l+LhhTbrH4raPxtZbf8Aw1rVx6uAdFm6Wa/J9PWZ538fykx8mz6LZb5dXpu8vbJPfYtptabfXj2uQxO06vcXb12jr7dRh393bjcH' \
                       + '0qECKAAAAAAAAAAAAAA8O/pBcbvXLp9JWZikaeMt9vC1r3tG3+nHxbrqI4TSmnz55rE5N6Ui3nG9Ztaft3j4Of8A6RXDLxl0urrE' \
                       + '93fDGG0+UXpe1o+MX/Y3HUXxuk0y6e1oi2SKZMUT52rE1vX38o+Erg9ecV1xaLvuC62IjnSMeSPSa3iXaxLXdI9H3+j1WKY37eDJ' \
                       + 'G3rtvHyQfLVrdqtbR9albfGIY9pXcNdsVYnxpNqT762mv8li0tIoySxrr1pWLoKJQlAEKoUK4BfxPSeqLS95r8M+VO1f3bVnb+Tz' \
                       + 'XD4va+ozQ721OaY5Ux0pE+tpmZ/hQevwAKAAAAAAAAAAAAAA03Szo7i4lpMulz8otzx5Ij8bFlj6N4/94TL5u4jwniHANVtel+xF' \
                       + '+1iy07Vcd4ieVsd48J9PH5vqpj63RYs9Jx58VMuO0bWpkrF6z9kg8e4P14460rXV6bJa8RtN68pn37bxLbf138PmOeDUe6YiGx4t' \
                       + '1P8AC802tipl0lp/sctrUj3UvvEfY4/inUXkjedJrcWSee1NRinHM/epv8io4HUWre2ovjiYx31WovjiY2mMd8k2pvHumGtyOy4l' \
                       + '0O1ugwXnXY6xvetaXpkjJS0RTaNp8fKPGHH6iNpUY9lmy5ZasCiUJlAJhMKd1UAyNNG9ofS/VTwzuOG4rTG1s8zln29nwr8v2vn7' \
                       + 'olwy2q1enwUjnkyRX3R5z9kRMvqzSYK4sePHSNqY6UpWPZWsbQir4jc3BIjdIAAAAAAAAAAAAAAAANV0m4VGs0ubBPjakzjn2ZI5' \
                       + '1l8x8b0VsOTJS9drVtatonymJ2fWEw8f65OjG141uGm9cnLP2a8q5IjlafZv84XDXit1qWTnpsxpEUShMqQSrqt7tl0f4Xk1eoxY' \
                       + 'MUb3yWiPbFY352n0jxQeudRnAezGXX5K7bTOHTzPtmI7do+O3xevd40PCNPTS4MOnxRtjxUiseU2nztPrM82dXNuK2PeJ7xg1uuR' \
                       + 'YGZFlcSxK2X6SC8IhIAAAAAAAAAAAAAACm9ItExaImJ8YmN4mFQDlOK9XfCtVM2y6GlbT9fDfJgn9yYhodR1M8Jn6P4VT0jUzaP3' \
                       + 'ol6SpsDyfN1K6D6up1cfexz/ALWPHUvoonnqdVMe/HH8nrlqLU4geZYOqDhlfpVz5PztRav8OzpODdEtJo940unri35WtG83mPW0' \
                       + 'zM/tdT3SYxA11NIvV07N7tVFAY1MK53a92U9kFqtF2tVUQkBKEgAAAAAAAAAAAAAAAAI2SApmDZUAp2TskBGxskBAkBAkAAAAAAA' \
                       + 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB//2Q=='

        return [
            {
                "input_type": "attached",
                "input_data": {
                    "images": [bucket_image_64, cup_image_64],
                    "image_types": ['jpg', 'jpg']
                },
                "output_type": "attached"
            }
        ]

    def post_load_initialize(self, service_manager: ServiceManager):

        # Load the graph model.
        graph_path = os.path.join(AGENT_DIRECTORY, 'model_data', 'classify_image_graph_def.pb')
        with tf.gfile.FastGFile(graph_path, 'rb') as f:
            self.graph_def = tf.GraphDef()
            self.graph_def.ParseFromString(f.read())
            tf.import_graph_def(self.graph_def, name='')

        # Create our long-running Tensorflow session
        self.session = tf.Session()

        # Save the softmax tensor which will run the model.
        self.softmax_tensor = self.session.graph.get_tensor_by_name('softmax:0')

        # Creates node ID --> English string lookup.
        self.node_lookup = NodeLookup()

    def perform(self, job: JobDescriptor):

        # Process the items in the job. A single job may include a request to classify
        # many different images. Each item, in turn, may include an array of images.
        results = []
        for job_item in job:

            # Make sure the input type is one we can handle...
            input_type = job_item['input_type']
            if input_type != 'attached':
                logger.error("BAD input dict %s", str(job_item))
                raise RuntimeError("TensorflowImageNet - job item 'input_type' must be 'attached'.")

            # Get the images to classify, while making sure our job item dict is of the appropriate format.
            input_data = job_item['input_data']
            if input_data is None:
                raise RuntimeError("TensorflowImageNet - job item 'input_data' must be defined.")
            images_to_classify = input_data.get('images')
            if images_to_classify is None:
                raise RuntimeError("TensorflowImageNet - job item 'input_data' missing 'images'")
            image_types = input_data.get('image_types')
            if image_types is None:
                raise RuntimeError("TensorflowImageNet - job item 'input_data' missing 'image_types'")

            # Clear the predictions for the new job item.
            predictions = []
            prediction_confidences = []

            # Classify all the images for this job item.
            for image, image_type in zip(images_to_classify, image_types):
                binary_image = base64.b64decode(image)
                if (image_type == 'jpeg' or image_type == 'jpg'):
                    decoder_key = 'DecodeJpeg/contents:0'
                elif (image_type == 'png'):
                    decoder_key = 'DecodeJpeg/contents:0'
                elif (image_type == 'gif'):
                    decoder_key = 'DecodeGif/contents:0'
                    raise RuntimeError("TensorflowImageNet - cannot decode gif images")
                elif (image_type == 'bmp'):
                    decoder_key = 'DecodeBmp/contents:0'
                    raise RuntimeError("TensorflowImageNet - cannot decode bmp images")
                else:
                    decoder_key = 'DecodeJpeg/contents:0'
                    logger.warn("Missing image type {0}".format(image_type))

                raw_predictions = self.session.run(self.softmax_tensor, {decoder_key: binary_image})

                logger.debug("classifying '{0}' image".format(image_type))

                # Pull the predicted scorces out of the raw predictions.
                predicted_scores = raw_predictions[0]

                # Sort and strip off the top 5 predictions.
                top_predictions = predicted_scores.argsort()[-5:][::-1]
                image_predictions = []
                image_scores = []
                for predicted_node_id in top_predictions:

                    # Get a text description for the top predicted node.
                    description = self.node_lookup.id_to_string(predicted_node_id)

                    # Cast to a float so JSON can serialize it. Normal Tensorflow float32 are not serializable.
                    score = float(predicted_scores[predicted_node_id])

                    logger.debug("        prediction = '{0}', score = {1}".format(description, score))

                    # Add only those that exceed our minimum score to the predictions and scores lists.
                    if (score > MINIMUM_SCORE):
                        image_predictions.append(description)
                        image_scores.append(score)

                # Append the filtered predictions and scores for this image.
                predictions.append(image_predictions)
                prediction_confidences.append(image_scores)

            # Add the job results to our combined results array for all job items.
            single_job_result = {
                'predictions': predictions,
                'confidences': prediction_confidences,
            }
            results.append(single_job_result)

        return results
