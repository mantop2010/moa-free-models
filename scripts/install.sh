#!/bin/bash
# MoA Free Models - Installation Script
# Usage: bash install.sh

echo "🔧 MoA Free Models — Installation"
echo "================================="
echo ""

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 18+ first."
    exit 1
fi
echo "✅ Node.js $(node --version) found"

# Check .env
ENV_FILE="$HOME/.hermes/.env"
if [ ! -f "$ENV_FILE" ]; then
    echo "⚠️  .env file not found at $ENV_FILE"
    echo "   Create it or add OPENCODE_ZEN_API_KEY manually"
fi

# Check if key is set
if grep -q "OPENCODE_ZEN_API_KEY" "$ENV_FILE" 2>/dev/null && ! grep -q "# OPENCODE_ZEN_API_KEY" "$ENV_FILE" 2>/dev/null; then
    echo "✅ OPENCODE_ZEN_API_KEY found in .env"
else
    echo ""
    echo "⚠️  OPENCODE_ZEN_API_KEY not set."
    echo "   Get your free key from: https://opencode.ai/auth"
    echo "   Then add to $ENV_FILE:"
    echo "   OPENCODE_ZEN_API_KEY=your_key_here"
fi

# Configure Hermes
echo ""
echo "🔄 Setting provider to opencode-zen..."
hermes config set model.provider opencode-zen 2>/dev/null

echo ""
echo "✅ Installation complete!"
echo ""
echo "📝 Next steps:"
echo "   1. Restart your session: /reset"
echo "   2. Test MoA: hermes chat -q 'What is 2+2?'"
echo ""
echo "📖 Documentation: skill_view(name='moa-free-models')"
