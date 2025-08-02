set -euo pipefail
shopt -s nullglob            # 該当ファイルが無ければ空リスト

BOOTSTRAP=1000               # --B の値を一括で変える場合はここを修正
PYTHON_CMD="python"          # python3 を明示したい場合は変更

for matches in *_matches.csv; do
    elos="${matches/_matches.csv/_elos.csv}"

    echo "▶︎ $matches → $elos"
    $PYTHON_CMD elo_fixed_ci.py \
        --file "$matches" \
        --B "$BOOTSTRAP" \
        --out "$elos"

    echo "✓ 完了: $elos"
done
