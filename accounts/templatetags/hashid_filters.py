from django import template
from hashids import Hashids

register = template.Library()
hashids = Hashids(salt="your_unique_salt_here", min_length=15)

@register.filter(name='hashid_encode')
def hashid_encode(value):
    return hashids.encode(value)

def encode_id(id):
    return hashids.encode(id)

def decode_id(hashid):
    decoded = hashids.decode(hashid)
    if decoded:
        return decoded[0]

    return None