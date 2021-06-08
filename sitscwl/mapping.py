from sbg import cwl

SCHEMA_TYPE_MAPPING = {
    "File": cwl.File,
    "string": cwl.String,
    "float": cwl.Float,
    "int": cwl.Int,
    "Directory": cwl.Dir
}


def guess_type(type_name):
    if type_name not in set(list(SCHEMA_TYPE_MAPPING.keys())):
        raise RuntimeError(f"Invalid type for this workflow: {type_name}")

    return SCHEMA_TYPE_MAPPING[type_name]
