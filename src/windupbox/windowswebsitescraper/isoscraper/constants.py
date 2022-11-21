SUPPORTED_WINDOWS_VERSIONS = [
    'Windows 7',
    'Windows 8',
    'Windows 10',
    'Windows 11'
]

WINDOWS_VERSION_IDENT_MAPPING = {
    'Windows 7': None,
    'Windows 8': 'windows8ISO',
    'Windows 10': 'windows10ISO',
    'Windows 11': 'windows11'
}


KOREAN_ADDITIONAL = 0x20000
CHINA_ADDITIONAL = 0x10000


WINDOWS_7_DOWNLOAD_LINKS = {
    'SP1': {
        'version': 'SP1',
        'build': None,
        'release': None,
        'editions': {
            'Ultimate': {
                'x64': r"https://download.microsoft.com/download/5/1/9/5195A765-3A41-4A72-87D8-200D897CBE21/7601.24214.180801-1700.win7sp1_ldr_escrow_CLIENT_ULTIMATE_x64FRE_en-us.iso",
                'x86': r"https://download.microsoft.com/download/1/E/6/1E6B4803-DD2A-49DF-8468-69C0E6E36218/7601.24214.180801-1700.win7sp1_ldr_escrow_CLIENT_ULTIMATE_x86FRE_en-us.iso"
            },
            'Professional': {
                'x64': r"https://download.microsoft.com/download/0/6/3/06365375-C346-4D65-87C7-EE41F55F736B/7601.24214.180801-1700.win7sp1_ldr_escrow_CLIENT_PROFESSIONAL_x64FRE_en-us.iso",
                'x86': r"https://download.microsoft.com/download/C/0/6/C067D0CD-3785-4727-898E-60DC3120BB14/7601.24214.180801-1700.win7sp1_ldr_escrow_CLIENT_PROFESSIONAL_x86FRE_en-us.iso"
            },
            'Home Premium': {
                'x64': r"https://download.microsoft.com/download/E/A/8/EA804D86-C3DF-4719-9966-6A66C9306598/7601.24214.180801-1700.win7sp1_ldr_escrow_CLIENT_HOMEPREMIUM_x64FRE_en-us.iso",
                'x86': r"https://download.microsoft.com/download/E/D/A/EDA6B508-7663-4E30-86F9-949932F443D0/7601.24214.180801-1700.win7sp1_ldr_escrow_CLIENT_HOMEPREMIUM_x86FRE_en-us.iso"
            }
        }
    }
}


WINDOWS_8_CODES = {
    'Update 3': {
        'version': 'Update 3',
        'build': '9600',
        'release': None,
        'editions': {
            'Standard': 52,
            'N': 55,
            'Single Language': 48,
            'K': None,  # KOREAN_ADDITIONAL+61,
            'KN': None,  # KOREAN_ADDITIONAL+62,
        }
    }
}


WINDOWS_10_CODES = {
    '1507': {
        'version': '1507',
        'build': '10240.16384',
        'release': '2015.07',
        'editions': {
            'Home': 79,
            'Pro': 79,
            'Home N': 81,
            'Pro N': 81,
            'Single Language': 82,
            'Education': 75,
            'Education N': 77,
            'KN': None,  # KOREAN_ADDITIONAL+80,
            'Education KN': None,  # KOREAN_ADDITIONAL+76,
            'China Get Genuine': None,  # CHINA_ADDITIONAL+78
        }
    },
    '1511 R1': {
        'version': '1511 R1',
        'build': '10586.0',
        'release': '2015.11',
        'editions': {
            'Home': 99,
            'Pro': 99,
            'Home N': 105,
            'Pro N': 105,
            'Single Language': 106,
            'Education': 100,
            'Education N': 102,
            'KN': None,  # KOREAN_ADDITIONAL + 104,
            'Education KN': None,  # KOREAN_ADDITIONAL + 101,
            'China Get Genuine': None,  # CHINA_ADDITIONAL + 103
        }
    },
    '1511 R2': {
        'version': '1511 R2',
        'build': '10586.104',
        'release': '2016.02',
        'editions': {
            'Home': 109,
            'Pro': 109,
            'Home N': 115,
            'Pro N': 115,
            'Single Language': 116,
            'Education': 110,
            'Education N': 112,
            'KN': None,  # KOREAN_ADDITIONAL + 114,
            'Education KN': None,  # KOREAN_ADDITIONAL + 111,
            'China Get Genuine': None,  # CHINA_ADDITIONAL + 113
        }
    },
    '1511 R3': {
        'version': '1511 R3',
        'build': '10586.164',
        'release': '2016.04',
        'editions': {
            'Home': 178,
            'Pro': 178,
            'Home N': 183,
            'Pro N': 183,
            'Single Language': 184,
            'Education': 179,
            'Education N': 181,
            'KN': None,  # KOREAN_ADDITIONAL + 182,
            'Education KN': None,  # KOREAN_ADDITIONAL + 180,
            'China Get Genuine': None,  # CHINA_ADDITIONAL + 185
        }
    },
    '1607': {
        'version': '1607',
        'build': '14393.0',
        'release': '2016.07',
        'editions': {
            'Home': 244,
            'Pro': 244,
            'Home N': 245,
            'Pro N': 245,
            'Single Language': 246,
            'Education': 242,
            'Education N': 243,
            'KN': None,
            'Education KN': None,
            'China Get Genuine': None,  # CHINA_ADDITIONAL + 247
        }
    },
    '1703': {
        'version': '1703',
        'build': '15063.0',
        'release': '2017.03',
        'editions': {
            'Home': 361,
            'Pro': 361,
            'Home N': 362,
            'Pro N': 362,
            'Single Language': 363,
            'Education': 423,
            'Education N': 424,
            'KN': None,
            'Education KN': None,
            'China Get Genuine': None,  # CHINA_ADDITIONAL + 364
        }
    },
    '1709': {
        'version': '1709',
        'build': '16299.15',
        'release': '2017.09',
        'editions': {
            'Home': 484,
            'Pro': 484,
            'Home N': None,
            'Pro N': None,
            'Single Language': None,
            'Education': 488,
            'Education N': None,
            'KN': None,
            'Education KN': None,
            'China Get Genuine': None,  # CHINA_ADDITIONAL + 485
        }
    },
    '1803': {
        'version': '1803',
        'build': '17134.1',
        'release': '2018.04',
        'editions': {
            'Home': 651,
            'Pro': 651,
            'Home N': None,
            'Pro N': None,
            'Single Language': None,
            'Education': 655,
            'Education N': None,
            'KN': None,
            'Education KN': None,
            'China Get Genuine': None,  # CHINA_ADDITIONAL + 652,
            '1803': 637
        }
    },
    '1809 R1': {
        'version': '1809 R1',
        'build': '17763.1',
        'release': '2018.09',
        'editions': {
            'Home': 1019,
            'Pro': 1019,
            'Home N': None,
            'Pro N': None,
            'Single Language': None,
            'Education': 1021,
            'Education N': None,
            'KN': None,
            'Education KN': None,
            'China Get Genuine': None,  # CHINA_ADDITIONAL + 1020,
        }
    },
    '1809 R2': {
        'version': '1809 R2',
        'build': '17763.107',
        'release': '2018.10',
        'editions': {
            'Home': 1060,
            'Pro': 1060,
            'Home N': None,
            'Pro N': None,
            'Single Language': None,
            'Education': 1056,
            'Education N': None,
            'KN': None,
            'Education KN': None,
            'China Get Genuine': None,  # CHINA_ADDITIONAL + 1061,
        }
    },
    '1809 R3': {
        'version': '1809 R3',
        'build': '17763.379',
        'release': '2019.03',
        'editions': {
            'Home': 1203,
            'Pro': 1203,
            'Home N': None,
            'Pro N': None,
            'Single Language': None,
            'Education': 1202,
            'Education N': None,
            'KN': None,
            'Education KN': None,
            'China Get Genuine': None,  # CHINA_ADDITIONAL + 1204,
        }
    },
    '19H1 2019.05': {
        'version': '19H1 2019.05',
        'build': '18362.30',
        'release': '2019.05',
        'editions': {
            'Home': 1214,
            'Pro': 1214,
            'Home N': None,
            'Pro N': None,
            'Single Language': None,
            'Education': 1216,
            'Education N': None,
            'KN': None,
            'Education KN': None,
            'China Get Genuine': None,  # CHINA_ADDITIONAL + 1215,
        }
    },
    '19H1 2019.09': {
        'version': '19H1 2019.09',
        'build': '18362.356',
        'release': '2019.09',
        'editions': {
            'Home': 1384,
            'Pro': 1384,
            'Home N': None,
            'Pro N': None,
            'Single Language': None,
            'Education': 1386,
            'Education N': None,
            'KN': None,
            'Education KN': None,
            'China Get Genuine': None,  # CHINA_ADDITIONAL + 1385,
        }
    },
    '19H2': {
        'version': '19H2',
        'build': '18363.418',
        'release': '2019.11',
        'editions': {
            'Home': 1429,
            'Pro': 1429,
            'Home N': None,
            'Pro N': None,
            'Single Language': None,
            'Education': 1431,
            'Education N': None,
            'KN': None,
            'Education KN': None,
            'China Get Genuine': None,  # CHINA_ADDITIONAL + 1430,
        }
    },
    '20H1': {
        'version': '20H1',
        'build': '19041.264',
        'release': '2020.05',
        'editions': {
            'Home': 1626,
            'Pro': 1626,
            'Home N': None,
            'Pro N': None,
            'Single Language': None,
            'Education': 1625,
            'Education N': None,
            'KN': None,
            'Education KN': None,
            'China Get Genuine': None,  # CHINA_ADDITIONAL + 1627,
        }
    },
    '20H2 2020.10': {
        'version': '20H2 2020.10',
        'build': '19042.508',
        'release': '2020.10',
        'editions': {
            'Home': 1807,
            'Pro': 1807,
            'Home N': None,
            'Pro N': None,
            'Single Language': None,
            'Education': 1805,
            'Education N': None,
            'KN': None,
            'Education KN': None,
            'China Get Genuine': None,  # CHINA_ADDITIONAL + 1806,
        }
    },
    '21H1': {
        'version': '21H1',
        'build': '19043.985',
        'release': '2021.05',
        'editions': {
            'Home': 2033,
            'Pro': 2033,
            'Home N': None,
            'Pro N': None,
            'Single Language': None,
            'Education': 2032,
            'Education N': None,
            'KN': None,
            'Education KN': None,
            'China Get Genuine': None,  # CHINA_ADDITIONAL + 2034,
        }
    },
    '21H2': {
        'version': '21H2',
        'build': '19044.1288',
        'release': '2021.11',
        'editions': {
            'Home': 2084,
            'Pro': 2084,
            'Home N': None,
            'Pro N': None,
            'Single Language': None,
            'Education': 2084,
            'Education N': None,
            'KN': None,
            'Education KN': None,
            'China Get Genuine': None,  # CHINA_ADDITIONAL + 2085,
        }
    },
}

WINDOWS_10_DOWNLOAD_LINKS = {
    'Enterprise Evaluation': {
        'editions': {
            'Enterprise Evaluation': {
                'x64': 'http://download.microsoft.com/download/C/3/9/C399EEA8-135D-4207-92C9-6AAB3259F6EF/10240.16384.150709-1700.TH1_CLIENTENTERPRISEEVAL_OEMRET_X64FRE_EN-US.ISO'
            }
        }
    }
}

WINDOWS_11_CODES = {
    '21H2 v1': {
        'version': '21H2 v1',
        'build': '22000.318',
        'release': '2021.11',
        'editions': {
            'Home': 2093,
            'Pro': 2093,
            'Edu': 2093,
            'Home China': None,  # CHINA_ADDITIONAL + 2094,
        }
    },
    '21H2': {
        'version': '21H2',
        'build': '22000.194',
        'release': '2021.10',
        'editions': {
            'Home': 2069,
            'Pro': 2069,
            'Edu': 2069,
            'Home China': None, #CHINA_ADDITIONAL + 2070,
        }
    },
}


WINDOWS_CODE_MAPPING = {
    'Windows 7': None,
    'Windows 8': WINDOWS_8_CODES,
    'Windows 10': WINDOWS_10_CODES,
    'Windows 11': WINDOWS_11_CODES
}

WINDOWS_LINK_MAPPING = {
    'Windows 7': WINDOWS_7_DOWNLOAD_LINKS,
    'Windows 8': None,
    'Windows 10': WINDOWS_10_DOWNLOAD_LINKS,
    'Windows 11': None
}


LANGUAGE_SELECTION_PAGE_ID = r"a8f8f489-4c7f-463a-9ca6-5cff94d8d041"
DOWNLOAD_PAGE_ID = r"a224afab-2097-4dfa-a2ba-463eb191a285"

# ARCHITECTURE_X86 = 'IsoX86'
# ARCHITECTURE_X64 = 'IsoX64'

ARCHITECTURE_MAPPING = {
    'IsoX86': 'x86',
    'IsoX64': 'x64'
}



