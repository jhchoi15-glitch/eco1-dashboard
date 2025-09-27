// static/script.js

document.addEventListener('DOMContentLoaded', () => {
    // --- 기존 알림 기능 ---
    const notificationBtn = document.getElementById('notification-btn');
    const notificationContainer = document.getElementById('notification-container');
    const messages = [
        "🔔 새로운 영업 DB 5건이 추가되었습니다.", "📈 이번 주 팀 리포트가 업데이트 되었습니다.",
        "🗓️ 오후 3시에 '엔터프라이즈' 관련 미팅이 있습니다.", "✅ '플라이이디' 데이터 조회가 완료되었습니다.",
        "💡 신규 경쟁사 'Next-Commerce' 정보가 등록되었습니다."
    ];
    if (notificationBtn) {
        notificationBtn.addEventListener('click', (event) => {
            event.preventDefault(); 
            const randomMessage = messages[Math.floor(Math.random() * messages.length)];
            const notification = document.createElement('div');
            notification.className = 'toast-notification';
            notification.textContent = randomMessage;
            notificationContainer.appendChild(notification);
            setTimeout(() => { notification.remove(); }, 4000);
        });
    }

    // --- n8n 연동 및 팝업 기능 ---
    const searchBtn = document.getElementById('search-btn');
    const mallIdInput = document.getElementById('mall-id-input');
    const resultArea = document.getElementById('search-result-area');
    
    const modal = document.getElementById('result-modal');
    const closeBtn = document.querySelector('.close-btn');

    // 팝업창 닫기 이벤트
    if(modal) {
        closeBtn.addEventListener('click', () => modal.classList.remove('show'));
        modal.addEventListener('click', (e) => {
            if (e.target === modal) modal.classList.remove('show');
        });
    }

    // 숫자 포맷팅 헬퍼 함수 (예: 10000 -> 10,000)
    const formatNumber = (num) => num.toLocaleString('ko-KR');

    // 조회 버튼 클릭 이벤트
    if (searchBtn) {
        searchBtn.addEventListener('click', () => {
            const mallId = mallIdInput.value;
            if (!mallId) {
                alert('몰아이디를 입력해주세요.');
                return;
            }
            resultArea.textContent = 'n8n 워크플로우 실행 중...';

            fetch('/run-workflow', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ mall_id: mallId })
            })
            .then(response => {
                if (!response.ok) throw new Error('서버 응답에 문제가 발생했습니다.');
                return response.json();
            })
            .then(data => {
                resultArea.textContent = ''; // 로딩 메시지 제거
                
                // [수정] n8n이 보내주는 [결과1, 결과2] 구조에 맞게 수정
                const summary = data[0];
                const best = data[1];

                if (!summary || !best) {
                    alert('데이터를 받아오는 데 실패했습니다. n8n 워크플로우를 확인해주세요.');
                    return;
                }

                // 2. 데이터 계산
                const revenue = Math.round(summary.total_order_amount_last_90_days / 3);
                const orders = Math.round(summary.total_buyer_count_last_90_days / 3);
                const visitors = Math.round(summary.total_all_visit_last_90_days / 3);
                const pv = (summary.total_page_view_last_90_days / 3).toFixed(1);
                
                const conversion = visitors > 0 
                    ? ((summary.total_buyer_count_last_90_days / summary.total_all_visit_last_90_days) * 100).toFixed(2)
                    : 0;

                const aov = orders > 0
                    ? Math.round(summary.total_order_amount_last_90_days / summary.total_buyer_count_last_90_days)
                    : 0;

                const bestPrice = best.total_order_count > 0 
                    ? Math.round(best.total_order_amount / best.total_order_count) 
                    : 0;

                // 3. 팝업창에 데이터 채우기
                document.getElementById('modal-mall-id').textContent = mallId;
                document.getElementById('metric-revenue').textContent = formatNumber(revenue);
                document.getElementById('metric-orders').textContent = formatNumber(orders);
                document.getElementById('metric-visitors').textContent = formatNumber(visitors);
                document.getElementById('metric-pv').textContent = pv;
                document.getElementById('metric-conversion').textContent = conversion;
                document.getElementById('metric-aov').textContent = formatNumber(aov);

                document.getElementById('best-name').textContent = best.product_name;
                document.getElementById('best-price').textContent = formatNumber(bestPrice);
                document.getElementById('best-basket').textContent = formatNumber(best.total_basket_count);
                document.getElementById('best-purchase').textContent = formatNumber(best.total_order_count);
                document.getElementById('best-amount').textContent = formatNumber(best.total_order_amount);
                document.getElementById('best-link').href = best.product_url;

                // 4. 팝업창 보여주기
                modal.classList.add('show');
            })
            .catch(error => {
                console.error('Error:', error);
                resultArea.textContent = '오류가 발생했습니다. 브라우저 콘솔(F12)을 확인하세요.';
            });
        });
    }
});