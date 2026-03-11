#!/usr/bin/env bash
# Sec-LLM OpenClaw Skill 调用辅助脚本
# 用法: ./call-sec-llm.sh <action> [args...]
# action: enrich | phishing | code-audit | rule | report-explain | chat
# 注: 威胁情报 report 需传入 enrich 完整 JSON，建议用 curl 直接调用

set -e
BASE_URL="${SEC_LLM_BASE_URL:-http://localhost:8000}"
API_KEY="${SEC_LLM_SKILL_API_KEY}"

if [ -z "$API_KEY" ]; then
  echo '{"error": "SEC_LLM_SKILL_API_KEY 未设置"}'
  exit 1
fi

ACTION="$1"
shift || true

case "$ACTION" in
  enrich)
    IOC="$1"
    [ -z "$IOC" ] && echo '{"error": "需要 ioc 参数"}' && exit 1
    BODY=$(jq -n --arg i "$IOC" '{ioc: $i, ioc_type: "auto"}' 2>/dev/null || echo "{\"ioc\": \"$(echo "$IOC" | sed 's/"/\\"/g')\", \"ioc_type\": \"auto\"}")
    curl -sS "${BASE_URL}/api/security-tools/threat-intel/enrich" \
      -H "X-Skill-Api-Key: $API_KEY" \
      -H "Content-Type: application/json" \
      -d "$BODY"
    ;;
  phishing)
    CONTENT="$1"
    [ -z "$CONTENT" ] && echo '{"error": "需要邮件内容"}' && exit 1
    # 支持从文件读取
    if [ -f "$CONTENT" ]; then
      BODY=$(jq -Rs '{content: .}' "$CONTENT" 2>/dev/null || echo "{\"content\": \"$(cat "$CONTENT" | sed 's/"/\\"/g' | tr '\n' ' ')\"}")
    else
      BODY="{\"content\": \"$CONTENT\"}"
    fi
    curl -sS "${BASE_URL}/api/security-tools/phishing-analyzer" \
      -H "X-Skill-Api-Key: $API_KEY" \
      -H "Content-Type: application/json" \
      -d "$BODY"
    ;;
  code-audit)
    CODE="$1"
    LANG="${2:-python}"
    [ -z "$CODE" ] && echo '{"error": "需要代码内容或文件路径"}' && exit 1
    if [ -f "$CODE" ]; then
      CODE=$(cat "$CODE")
    fi
    curl -sS "${BASE_URL}/api/security-tools/code-audit" \
      -H "X-Skill-Api-Key: $API_KEY" \
      -H "Content-Type: application/json" \
      -d "{\"code\": $(echo "$CODE" | jq -Rs .), \"language\": \"$LANG\"}"
    ;;
  rule)
    REQ="$*"
    [ -z "$REQ" ] && echo '{"error": "需要需求描述"}' && exit 1
    BODY=$(jq -n --arg r "$REQ" '{requirement: $r, rule_type: "yara"}' 2>/dev/null || echo "{\"requirement\": \"$(echo "$REQ" | sed 's/"/\\"/g')\", \"rule_type\": \"yara\"}")
    curl -sS "${BASE_URL}/api/security-tools/rule-generator" \
      -H "X-Skill-Api-Key: $API_KEY" \
      -H "Content-Type: application/json" \
      -d "$BODY"
    ;;
  report-explain)
    CONTENT="$1"
    [ -z "$CONTENT" ] && echo '{"error": "需要报告内容或文件路径"}' && exit 1
    if [ -f "$CONTENT" ]; then
      BODY=$(jq -Rs '{content: .}' "$CONTENT" 2>/dev/null || echo "{\"content\": \"$(cat "$CONTENT" | sed 's/"/\\"/g' | tr '\n' ' ')\"}")
    else
      BODY="{\"content\": \"$CONTENT\"}"
    fi
    curl -sS "${BASE_URL}/api/security-tools/report-explainer" \
      -H "X-Skill-Api-Key: $API_KEY" \
      -H "Content-Type: application/json" \
      -d "$BODY"
    ;;
  chat)
    MSG="$*"
    [ -z "$MSG" ] && echo '{"error": "需要消息内容"}' && exit 1
    BODY=$(jq -n --arg m "$MSG" '{message: $m, history: [], rag_only: false}' 2>/dev/null || echo "{\"message\": \"$(echo "$MSG" | sed 's/"/\\"/g')\", \"history\": [], \"rag_only\": false}")
    curl -sS "${BASE_URL}/api/chat" \
      -H "X-Skill-Api-Key: $API_KEY" \
      -H "Content-Type: application/json" \
      -d "$BODY"
    ;;
  *)
    echo "用法: $0 <enrich|phishing|code-audit|rule|report-explain|chat> [参数...]"
    exit 1
    ;;
esac
