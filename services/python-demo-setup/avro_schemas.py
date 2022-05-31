randomuser_avro_schema = '''{
  "name": "flatRandomuser",
  "type": "record",
  "namespace": "nifi",
  "fields": [
    {
      "name": "results",
      "type": {
        "type": "array",
        "items": {
          "name": "resultsrecord",
          "type": "record",
          "fields": [
            {
              "name": "gender",
              "type": "string"
            },
            {
              "name": "name_title",
              "type": "string"
            },
            {
              "name": "name_first",
              "type": "string"
            },
            {
              "name": "name_last",
              "type": "string"
            },
            {
              "name": "location_street_number",
              "type": "int"
            },
            {
              "name": "location_street_name",
              "type": "string"
            },
            {
              "name": "location_city",
              "type": "string"
            },
            {
              "name": "location_state",
              "type": "string"
            },
            {
              "name": "location_country",
              "type": "string"
            },
            {
              "name": "location_postcode",
              "type": "string"
            },
            {
              "name": "location_coordinates_latitude",
              "type": "string"
            },
            {
              "name": "location_coordinates_longitude",
              "type": "string"
            },
            {
              "name": "location_timezone_offset",
              "type": "string"
            },
            {
              "name": "location_timezone_description",
              "type": "string"
            },
            {
              "name": "email",
              "type": "string"
            },
            {
              "name": "login_uuid",
              "type": "string"
            },
            {
              "name": "login_username",
              "type": "string"
            },
            {
              "name": "login_password",
              "type": "string"
            },
            {
              "name": "login_salt",
              "type": "string"
            },
            {
              "name": "login_md5",
              "type": "string"
            },
            {
              "name": "login_sha1",
              "type": "string"
            },
            {
              "name": "login_sha256",
              "type": "string"
            },
            {
              "name": "dob_date",
              "type": "string"
            },
            {
              "name": "dob_age",
              "type": "int"
            },
            {
              "name": "registered_date",
              "type": "string"
            },
            {
              "name": "registered_age",
              "type": "int"
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
              "name": "id_name",
              "type": "string"
            },
            {
              "name": "id_value",
              "type": "string"
            },
            {
              "name": "picture_large",
              "type": "string"
            },
            {
              "name": "picture_medium",
              "type": "string"
            },
            {
              "name": "picture_thumbnail",
              "type": "string"
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
      "name": "info_seed",
      "type": "string"
    },
    {
      "name": "info_results",
      "type": "int"
    },
    {
      "name": "info_page",
      "type": "int"
    },
    {
      "name": "info_version",
      "type": "string"
    }
  ]
}'''
