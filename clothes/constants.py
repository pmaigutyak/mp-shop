
from django.utils.translation import ugettext_lazy as _


SEX_MALE = 'male'
SEX_FEMALE = 'female'
SEX_BOTH = 'both'


SEX_CHOICES = (
    (SEX_MALE, _('Male')),
    (SEX_FEMALE, _('Female')),
    (SEX_BOTH, _('Both')),
)


DEFAULT_CLOTHES_SIZES = {
    'male': {
        44: {
            'neck_volume': 39,
            'breast_size': 88,
            'product_length': 74
        },
        46: {
            'neck_volume': 40,
            'breast_size': 92,
            'product_length': 76
        },
        48: {
            'neck_volume': 41,
            'breast_size': 98,
            'product_length': 77
        },
        50: {
            'neck_volume': 42,
            'breast_size': 108,
            'product_length': 80
        },
        52: {
            'neck_volume': 43,
            'breast_size': 112,
            'product_length': 80
        },
        54: {
            'neck_volume': 44,
            'breast_size': 116,
            'product_length': 80
        },
        56: {
            'neck_volume': 45,
            'breast_size': 124,
            'product_length': 80
        },
        58: {
            'neck_volume': 46,
            'breast_size': 130,
            'product_length': 82
        },
        60: {
            'neck_volume': 47,
            'breast_size': 136,
            'product_length': 82
        },
        62: {
            'neck_volume': 48,
            'breast_size': 142,
            'product_length': 82
        }
    },
    'female': {
        42: {
            'hips_volume': 92,
            'waist_volume': 63,
            'breast_size': 84
        },
        44: {
            'hips_volume': 96,
            'waist_volume': 68,
            'breast_size': 88
        },
        46: {
            'hips_volume': 100,
            'waist_volume': 72,
            'breast_size': 92
        },
        48: {
            'hips_volume': 104,
            'waist_volume': 76,
            'breast_size': 96
        },
        50: {
            'hips_volume': 108,
            'waist_volume': 80,
            'breast_size': 100
        },
        52: {
            'hips_volume': 112,
            'waist_volume': 84,
            'breast_size': 104
        },
        54: {
            'hips_volume': 116,
            'waist_volume': 89,
            'breast_size': 108
        },
        56: {
            'hips_volume': 120,
            'waist_volume': 94,
            'breast_size': 112
        },
        58: {
            'hips_volume': 124,
            'waist_volume': 99,
            'breast_size': 116
        },
        60: {
            'hips_volume': 128,
            'waist_volume': 104,
            'breast_size': 120
        }
    }
}


MALE_CLOTHES_FIELDS = [
    'size', 'breast_size', 'neck_volume', 'product_length',
    'waist_volume', 'hips_volume', 'sleeve_length', 'shoulder_length',
    'back_width'
]


FEMALE_CLOTHES_FIELDS = [
    'size', 'breast_size', 'waist_volume', 'hips_volume',
    'sleeve_length', 'shoulder_length', 'product_length', 'back_width',
    'length_of_dress_up_to_waist', 'length_of_dress_from_waist'
]


CLOTHES_FIELDS = {
    SEX_MALE: MALE_CLOTHES_FIELDS,
    SEX_FEMALE: FEMALE_CLOTHES_FIELDS
}
