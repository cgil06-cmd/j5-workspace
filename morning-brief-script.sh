#!/bin/zsh
# J5 Morning Brief
export GOG_KEYRING_BACKEND=file
export GOG_KEYRING_PASSPHRASE=""
export PATH="/opt/homebrew/bin:$PATH"

TODAY=$(date '+%A, %B %-d, %Y')
TOMORROW=$(date -v+1d '+%A, %B %-d')
TODAY_DATE=$(date '+%Y-%m-%d')
TOMORROW_DATE=$(date -v+1d '+%Y-%m-%d')
DAY_AFTER=$(date -v+2d '+%Y-%m-%d')

format_events() {
  local account=$1
  local from=$2
  local to=$3
  
  gog calendar events --account "$account" --from "$from" --to "$to" -p 2>/dev/null | grep -v "^ID\|^START\|^#" | while read -r line; do
    [[ -z "$line" ]] && continue
    id=$(echo "$line" | awk -F'\t' '{print $1}')
    start=$(echo "$line" | awk -F'\t' '{print $2}')
    summary=$(echo "$line" | awk -F'\t' '{print $4}')
    
    [[ ${#id} -gt 55 ]] && continue
    [[ "$id" == reclaim* ]] && continue
    [[ -z "$summary" ]] && continue
    
    if [[ "$start" == *T* ]]; then
      hour=$(echo "$start" | cut -c12-13)
      min=$(echo "$start" | cut -c15-16)
      hour_12=$((10#$hour % 12))
      [[ $hour_12 -eq 0 ]] && hour_12=12
      ampm="AM"
      [[ 10#$hour -ge 12 ]] && ampm="PM"
      time_str="${hour_12}:${min} ${ampm}"
    else
      time_str="All day"
    fi
    echo "  $time_str — $summary"
  done
}

echo "⚡ MORNING BRIEF — $TODAY"
echo ""
echo "📅 TODAY"
format_events cgilbert@ourgardencity.com "$TODAY_DATE" "$TOMORROW_DATE"
format_events cgil06@gmail.com "$TODAY_DATE" "$TOMORROW_DATE"
echo ""
echo "📅 TOMORROW ($TOMORROW)"
format_events cgilbert@ourgardencity.com "$TOMORROW_DATE" "$DAY_AFTER"
format_events cgil06@gmail.com "$TOMORROW_DATE" "$DAY_AFTER"
echo ""
