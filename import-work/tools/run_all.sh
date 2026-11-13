#!/bin/zsh
# build all pages, gate + offsets for each; prints failing rows only
export PATH=$HOME/.local/node/bin:$PATH
S=~/.claude/skills/eds-parity-rebuild/scripts
cd "$(dirname $0)/.."
P=(home our-company our-commitment our-company-sfntc-vision transforming-tobacco our-product-the-passion-behind-the-brand want-to-quit-smoking our-commitment-cigarette-waste our-commitment-carolina-farm-stewardship-association underage-tobacco-prevention our-product our-commitment-what-you-can-do-to-help sfntc-foundation)
python3 $S/build.py --project . $P _nav _footer > /dev/null
for n in $P; do
  echo "## $n"
  node $S/gate.js ${1:-gate}/$n.json 2>&1 | grep "FAIL\|rror\|PASS ->" | cut -c1-120
  node $S/offsets.js ${1:-gate}/$n.json 2>&1 | tail -1
done
