#!/bin/bash
# setup-dvc-local.sh - Configure DVC with AWS credentials for local development

echo "🔐 Configuring DVC with AWS credentials..."

# Check if credentials are set in environment
if [ -z "$AWS_ACCESS_KEY_ID" ] || [ -z "$AWS_SECRET_ACCESS_KEY" ]; then
    echo "❌ Error: AWS credentials not found in environment variables"
    echo "Please set:"
    echo "  export AWS_ACCESS_KEY_ID='your_access_key'"
    echo "  export AWS_SECRET_ACCESS_KEY='your_secret_key'"
    exit 1
fi

# Create .dvc/config.local with credentials (Git ignores this)
cat > .dvc/config.local << EOF
['remote "myremote"']
    url = s3://2022bcd0013-mlops/mlops-assignment
    access_key_id = ${AWS_ACCESS_KEY_ID}
    secret_access_key = ${AWS_SECRET_ACCESS_KEY}
EOF

echo "✅ DVC configured with local credentials in .dvc/config.local"
echo "ℹ️  This file is in .gitignore and won't be committed"
echo ""
echo "Next steps:"
echo "  dvc pull          # Pull data from S3"
echo "  python src/train.py  # Train model"
