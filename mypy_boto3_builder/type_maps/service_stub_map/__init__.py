"""
Methods for boto3 injected methods.
"""
from mypy_boto3_builder.service_name import ServiceName, ServiceNameCatalog
from mypy_boto3_builder.structures.method import Method
from mypy_boto3_builder.type_maps.service_stub_map import dynamodb, ec2, rds, s3
from mypy_boto3_builder.utils.strings import get_typed_dict_name

ClassTypeMap = dict[str, list[Method]]
ServiceStubMap = dict[ServiceName, ClassTypeMap]

SERVICE_STUB_MAP: ServiceStubMap = {
    ServiceNameCatalog.ec2: {
        "Client": ec2.CLIENT_METHODS,
        "Instance": ec2.INSTANCE_METHODS,
        "DhcpOptions": ec2.COMMON_METHODS,
        "Image": ec2.COMMON_METHODS,
        "InternetGateway": ec2.COMMON_METHODS,
        "NetworkAcl": ec2.COMMON_METHODS,
        "NetworkInterface": ec2.COMMON_METHODS,
        "SecurityGroup": ec2.COMMON_METHODS,
        "Snapshot": ec2.COMMON_METHODS,
        "Volume": ec2.COMMON_METHODS,
        "RouteTable": ec2.COMMON_METHODS,
        "Subnet": ec2.COMMON_METHODS,
        "Vpc": ec2.COMMON_METHODS,
    },
    ServiceNameCatalog.dynamodb: {
        "Table": dynamodb.TABLE_METHODS,
    },
    ServiceNameCatalog.rds: {
        "Client": rds.CLIENT_METHODS,
    },
    ServiceNameCatalog.s3: {
        "Client": s3.CLIENT_METHODS,
        "Bucket": s3.BUCKET_METHODS,
        "Object": s3.OBJECT_METHODS,
    },
}


def get_stub_method_map(service_name: ServiceName, parent: str) -> dict[str, Method]:
    """
    Get boto3 injected methods.
    """
    methods = SERVICE_STUB_MAP.get(service_name, {}).get(parent, [])
    for method in methods:
        method.create_request_type_annotation(get_typed_dict_name(parent, method.name, "Request"))
    return {method.name: method for method in methods}
