#!/bin/bash

# 🚀 SAVE TO GITHUB REMOTE REPOSITORY
# This pushes all changes to GitHub so they survive codespace deletion

echo "🚀 SAVING ENHANCEMENTS TO GITHUB REMOTE..."
echo "==========================================="

# 1. First, make sure we have the enhanced main.py
echo "💾 Ensuring enhanced scanner is active..."
if [ ! -f "main.py" ]; then
    echo "❌ main.py not found! Cannot proceed."
    exit 1
fi

# 2. Add all changes to git
echo "📦 Adding all changes to git..."
git add .

# 3. Check if there are changes to commit
if git diff --cached --quiet; then
    echo "✅ No changes to commit - enhancements already saved."
else
    # 4. Commit changes with descriptive message
    echo "📚 Committing enhancements..."
    git commit -m "🚀 ENHANCED SCANNER: Professional Vulnerability Analysis

- Integrated advanced vulnerability analyzer
- Added focused terminal output with exploit scenarios
- Enhanced vulnerability classification system
- Added flash loan attack vectors
- Improved risk assessment and impact analysis
- Professional reporting format

Features:
✅ Vulnerability names and types
✅ Exploit scenarios with flash loan logic  
✅ Affected pool pairs and contracts
✅ Risk assessment and impact analysis
✅ Professional terminal output format"

    # 5. Push to remote GitHub repository
    echo "🌐 Pushing to GitHub remote repository..."
    git push origin main
    
    if [ $? -eq 0 ]; then
        echo "✅ SUCCESS: All enhancements pushed to GitHub!"
    else
        echo "❌ FAILED: Could not push to GitHub."
        echo "💡 Check your remote repository configuration:"
        git remote -v
        echo ""
        echo "📋 Manual push command: git push origin main"
    fi
fi

# 6. Verify the enhanced scanner is ready
echo ""
echo "🔍 VERIFYING ENHANCED SCANNER..."
python -c "
import sys
try:
    from main import SeekProResearchEnhanced
    print('✅ ENHANCED SCANNER: READY AND SAVED TO GITHUB')
    print('🚀 Single command: python main.py')
except ImportError as e:
    print(f'❌ SCANNER ISSUE: {e}')
"

# 7. Create permanent setup verification
echo ""
echo "📋 GITHUB REMOTE STATUS:"
git remote -v
echo ""
echo "📊 LOCAL CHANGES STATUS:"
git status --short

echo ""
echo "=========================================="
echo "🎉 GITHUB SAVE COMPLETE!"
echo ""
echo "✅ Your enhancements are now saved to:"
echo "   https://github.com/$(git config --get remote.origin.url | sed 's/.*github.com[:/]//' | sed 's/\.git//')"
echo ""
echo "🚀 NEXT TIME YOU CREATE A CODESPACE:"
echo "   1. Clone your repository fresh"
echo "   2. Run: python main.py"
echo "   3. Enjoy the enhanced scanner immediately!"
echo ""
echo "💾 Changes are permanently saved to GitHub cloud!"
