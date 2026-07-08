import yaml
import os

env_path = '/home/holisticjson/.hermes/.env'
litellm_env_path = '/home/holisticjson/litellm/.env'
litellm_config_path = '/home/holisticjson/litellm/config.yaml'
profile_config_path = '/home/holisticjson/.hermes/profiles/aws_bedrock_coder/config.yaml'

# 1. Read variables from main Hermes .env
hermes_env = {}
if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        for line in f:
            if '=' in line and not line.strip().startswith('#'):
                k, v = line.strip().split('=', 1)
                hermes_env[k.strip()] = v.strip().strip('"').strip("'")

# 2. Write correct variables to LiteLLM .env
litellm_env_vars = {
    'AWS_ACCESS_KEY_ID': hermes_env.get('AWS_ACCESS_KEY_ID', ''),
    'AWS_SECRET_ACCESS_KEY': hermes_env.get('AWS_SECRET_ACCESS_KEY', ''),
    'AWS_REGION_NAME': 'eu-central-1',
    'AWS_REGION': 'eu-central-1',
    'GOOGLE_APPLICATION_CREDENTIALS': hermes_env.get('GOOGLE_APPLICATION_CREDENTIALS', ''),
    'GOOGLE_CLOUD_PROJECT': hermes_env.get('VERTEX_PROJECT', 'holistic-broker'),
    'GEMINI_API_KEY': 'AQ.Ab8RN6Icx0WTaJPGqSVUpcHqrLoGL8X_b9RPtV7uq1xwiNOPAg'
}

with open(litellm_env_path, 'w') as f:
    for k, v in litellm_env_vars.items():
        f.write(f'{k}="{v}"\n')
print("Updated LiteLLM .env with correct Bedrock, Vertex AI, and Gemini API credentials.")

# 3. Update LiteLLM config.yaml
if os.path.exists(litellm_config_path):
    with open(litellm_config_path, 'r') as f:
        config = yaml.safe_load(f) or {}
    
    # We redefine model_list to have correct, active models
    config['model_list'] = [
        {
            'model_name': 'hermes-fast',
            'litellm_params': {
                'model': 'vertex_ai/gemini-2.5-flash'
            }
        },
        {
            'model_name': 'hermes-think',
            'litellm_params': {
                'model': 'vertex_ai/gemini-2.5-pro'
            }
        },
        {
            'model_name': 'hermes-image',
            'litellm_params': {
                'model': 'vertex_ai/imagen-3.0-generate-001'
            }
        },
        {
            'model_name': 'gemini-3.5-flash',
            'litellm_params': {
                'model': 'gemini/gemini-3.5-flash'
            }
        },
        {
            'model_name': 'gemini-3.1-pro',
            'litellm_params': {
                'model': 'gemini/gemini-3.1-pro'
            }
        },
        {
            'model_name': 'bedrock/anthropic.claude-sonnet-4-6',
            'litellm_params': {
                'model': 'bedrock/eu.anthropic.claude-sonnet-4-6',
                'aws_region_name': 'eu-central-1'
            }
        },
        {
            'model_name': 'bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0',
            'litellm_params': {
                'model': 'bedrock/eu.anthropic.claude-sonnet-4-6',
                'aws_region_name': 'eu-central-1'
            }
        },
        {
            'model_name': 'bedrock/anthropic.claude-sonnet-4',
            'litellm_params': {
                'model': 'bedrock/eu.anthropic.claude-sonnet-4-6',
                'aws_region_name': 'eu-central-1'
            }
        }
    ]
    
    with open(litellm_config_path, 'w') as f:
        yaml.safe_dump(config, f, default_flow_style=False)
    print("Updated LiteLLM config.yaml with cross-region Bedrock prefixes, Gemini 3.5/3.1 mappings, and Vertex AI models.")

# 4. Update aws_bedrock_coder profile config.yaml
if os.path.exists(profile_config_path):
    with open(profile_config_path, 'r') as f:
        pconfig = yaml.safe_load(f) or {}
    
    pconfig['delegation'] = pconfig.get('delegation', {})
    pconfig['delegation']['model'] = 'bedrock/eu.anthropic.claude-sonnet-4-6'
    
    pconfig['fallback_model'] = {
        'provider': 'bedrock',
        'model': 'eu.anthropic.claude-3-5-sonnet-20241022-v2:0'
    }
    
    with open(profile_config_path, 'w') as f:
        yaml.safe_dump(pconfig, f, default_flow_style=False)
    print("Updated aws_bedrock_coder profile with cross-region model prefixes.")
