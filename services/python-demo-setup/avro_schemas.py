randomuser_avro_schema = '''{
    "name": "randomuser",
    "type": "record",
    "namespace": "nifi",
    "fields": [
        {
            "name": "results",
            "type": {
                "type": "array",
                "items": {
                    "name": "results_record",
                    "type": "record",
                    "fields": [
                        {
                            "name": "gender",
                            "type": "string"
                        },
                        {
                            "name": "name",
                            "type": {
                                "name": "name",
                                "type": "record",
                                "fields": [
                                    {
                                        "name": "title",
                                        "type": "string"
                                    },
                                    {
                                        "name": "first",
                                        "type": "string"
                                    },
                                    {
                                        "name": "last",
                                        "type": "string"
                                    }
                                ]
                            }
                        },
                        {
                            "name": "location",
                            "type": {
                                "name": "location",
                                "type": "record",
                                "fields": [
                                    {
                                        "name": "street",
                                        "type": {
                                            "name": "street",
                                            "type": "record",
                                            "fields": [
                                                {
                                                    "name": "number",
                                                    "type": "int"
                                                },
                                                {
                                                    "name": "name",
                                                    "type": "string"
                                                }
                                            ]
                                        }
                                    },
                                    {
                                        "name": "city",
                                        "type": "string"
                                    },
                                    {
                                        "name": "state",
                                        "type": "string"
                                    },
                                    {
                                        "name": "country",
                                        "type": "string"
                                    },
                                    {
                                        "name": "postcode",
                                        "type": "string"
                                    },
                                    {
                                        "name": "coordinates",
                                        "type": {
                                            "name": "coordinates",
                                            "type": "record",
                                            "fields": [
                                                {
                                                    "name": "latitude",
                                                    "type": "string"
                                                },
                                                {
                                                    "name": "longitude",
                                                    "type": "string"
                                                }
                                            ]
                                        }
                                    },
                                    {
                                        "name": "timezone",
                                        "type": {
                                            "name": "timezone",
                                            "type": "record",
                                            "fields": [
                                                {
                                                    "name": "offset",
                                                    "type": "string"
                                                },
                                                {
                                                    "name": "description",
                                                    "type": "string"
                                                }
                                            ]
                                        }
                                    }
                                ]
                            }
                        },
                        {
                            "name": "email",
                            "type": "string"
                        },
                        {
                            "name": "login",
                            "type": {
                                "name": "login",
                                "type": "record",
                                "fields": [
                                    {
                                        "name": "uuid",
                                        "type": "string"
                                    },
                                    {
                                        "name": "username",
                                        "type": "string"
                                    },
                                    {
                                        "name": "password",
                                        "type": "string"
                                    },
                                    {
                                        "name": "salt",
                                        "type": "string"
                                    },
                                    {
                                        "name": "md5",
                                        "type": "string"
                                    },
                                    {
                                        "name": "sha1",
                                        "type": "string"
                                    },
                                    {
                                        "name": "sha256",
                                        "type": "string"
                                    }
                                ]
                            }
                        },
                        {
                            "name": "dob",
                            "type": {
                                "name": "dob",
                                "type": "record",
                                "fields": [
                                    {
                                        "name": "date",
                                        "type": "string"
                                    },
                                    {
                                        "name": "age",
                                        "type": "int"
                                    }
                                ]
                            }
                        },
                        {
                            "name": "registered",
                            "type": {
                                "name": "registered",
                                "type": "record",
                                "fields": [
                                    {
                                        "name": "date",
                                        "type": "string"
                                    },
                                    {
                                        "name": "age",
                                        "type": "int"
                                    }
                                ]
                            }
                        },
                        {
                            "name": "phone",
                            "type": "string"
                        },
                        {
                            "name": "cell",
                            "type": "string"
                        },
                        {
                            "name": "id",
                            "type": {
                                "name": "id",
                                "type": "record",
                                "fields": [
                                    {
                                        "name": "name",
                                        "type": "string"
                                    },
                                    {
                                        "name": "value",
                                        "type": "string"
                                    }
                                ]
                            }
                        },
                        {
                            "name": "picture",
                            "type": {
                                "name": "picture",
                                "type": "record",
                                "fields": [
                                    {
                                        "name": "large",
                                        "type": "string"
                                    },
                                    {
                                        "name": "medium",
                                        "type": "string"
                                    },
                                    {
                                        "name": "thumbnail",
                                        "type": "string"
                                    }
                                ]
                            }
                        },
                        {
                            "name": "nat",
                            "type": "string"
                        }
                    ]
                }
            }
        },
        {
            "name": "info",
            "type": {
                "name": "info",
                "type": "record",
                "fields": [
                    {
                        "name": "seed",
                        "type": "string"
                    },
                    {
                        "name": "results",
                        "type": "int"
                    },
                    {
                        "name": "page",
                        "type": "int"
                    },
                    {
                        "name": "version",
                        "type": "string"
                    }
                ]
            }
        }
    ]
}'''
