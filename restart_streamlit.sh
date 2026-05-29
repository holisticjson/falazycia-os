#!/bin/bash
# restart_streamlit.sh — restartuje Streamlit z nowym app.py
pkill -u tomas_yq1b9su -f "streamlit run" 2>/dev/null || true
sleep 2
nohup /home/holisticjson/.local/bin/streamlit run /home/tomas_yq1b9su/Agentic_OS/dashboard/app.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    --server.headless true \
    > /tmp/streamlit.log 2>&1 &
echo $! > /tmp/streamlit.pid
sleep 4
if ss -tlnp | grep -q 8501; then
    echo "STREAMLIT_UP on 8501"
else
    echo "WAIT - checking again..."
    sleep 4
    ss -tlnp
fi
