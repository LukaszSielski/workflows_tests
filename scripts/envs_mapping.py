ENVS = {
    "apollo-dev": {
        "env": "dev",
        "tag": "VNXT CL Dev"
    },
    "apollo-dev-golden": {
        "env": "dev",
        "tag": "VNXT CL GOLDEN Dev"
    },
    "apollo-dev-iot": {
        "env": "dev",
        "tag": "VNXT CL IOT Dev"
    },
    "dev-us-east": {
        "env": "dev",
        "tag": "VNXT CL Dev"
    },
    "dev-us-west": {
        "env": "dev",
        "tag": "VNXT CL Dev"
    },
    "dev-iot-us-east": {
        "env": "dev",
        "tag": "VNXT CL IOT Dev"
    },
    "dev-iot-us-west": {
        "env": "dev",
        "tag": "VNXT CL IOT Dev"
    },
    "dev-golden-us-east": {
        "env": "dev",
        "tag": "VNXT CL GOLDEN Dev"
    },
    "dev-golden-us-west": {
        "env": "dev",
        "tag": "VNXT CL GOLDEN Dev"
    },
    "dev": {
        "env": "dev",
        "tag": "VNXT CL GOLDEN Dev"
    },
    "dev-iot": {
        "env": "dev",
        "tag": "VNXT CL IOT Dev"
    },
    "dev-golden": {
        "env": "dev",
        "tag": "VNXT CL GOLDEN Dev"
    },
    "iot": {
        "env": "dev",
        "tag": "VNXT CL IOT Dev"
    },
    "apollo-stage": {
        "env": "stage",
        "tag": "VNXT CL Stage"
    },
    "apollo-stage-iot": {
        "env": "stage",
        "tag": "VNXT CL IOT Stage"
    },
    "stage": {
        "env": "stage",
        "tag": "VNXT CL Stage"
    },
    "stage-east": {
        "env": "stage",
        "tag": "VNXT CL Stage"
    },
    "stage-west": {
        "env": "stage",
        "tag": "VNXT CL Stage"
    },
    "stage-iot": {
        "env": "stage",
        "tag": "VNXT CL IOT Stage"
    },
    "stage-ohio": {
        "env": "stage",
        "tag": "VNXT CL Stage"
    },
    "stage-ohio": {
        "env": "stage",
        "tag": "VNXT CL Stage"
    },
    "prod": {
        "env": "prod",
        "tag": "VNXT CL PROD"
    },
    "prod-east": {
        "env": "prod",
        "tag": "VNXT CL PROD"
    },
    "prod-west": {
        "env": "prod",
        "tag": "VNXT CL PROD"
    },
    "apollo-prod": {
        "env": "prod",
        "tag": "VNXT CL PROD"
    },
}

def get_tag(env: str) -> str:
    try:
        return ENVS[env]
    except KeyError:
        print(f"Mapping for {env} to tagging value not found!")
        raise Exception(f"Mapping for {env} to tagging value not found!")
