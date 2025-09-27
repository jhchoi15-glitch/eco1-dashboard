# app.py

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import datetime
import psycopg2 # pymysql 대신 psycopg2 임포트
import psycopg2.extras # DictCursor 사용을 위해 추가
from urllib.parse import urlparse # DB URL 파싱을 위해 추가
import os # 환경 변수 사용을 위해 추가
import requests
# config.py는 이제 직접 사용되지 않지만, 다른 잠재적 사용을 위해 남겨둘 수 있습니다.
# from config import DB_CONFIG 
import math 
import re
from collections import defaultdict
import decimal

app = Flask(__name__)

# 환경변수에서 시크릿 키를 가져오고, 없으면 기본값을 사용합니다.
app.secret_key = os.environ.get('SECRET_KEY', 'your_fallback_secret_key_123!') 

ALLOWED_USERS = {
    'jhchoi15': '최준환님',
    'jechoi02': '최주은님',
    'swlim': '임승우님',
    'hdkim03': '김혁동님',
    'htnoh': '노현탁님',
    'mhpark02': '박목화님'
}

# --- 수정: 렌더 데이터베이스 연결 함수 ---
def get_db_connection():
    # 렌더 환경 변수에 설정된 DATABASE_URL을 가져옵니다.
    db_url_str = os.environ.get("DATABASE_URL")
    if not db_url_str:
        raise ValueError("DATABASE_URL 환경 변수가 설정되지 않았습니다.")
    
    db_url = urlparse(db_url_str)
    conn = psycopg2.connect(
        dbname=db_url.path[1:],
        user=db_url.username,
        password=db_url.password,
        host=db_url.hostname,
        port=db_url.port
    )
    return conn


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        if user_id in ALLOWED_USERS:
            session['user_id'] = user_id
            return redirect(url_for('dashboard'))
        else:
            flash('ID를 다시 입력 해주세요')
            return redirect(url_for('login'))
    
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


def build_query(base_query, params_dict):
    """Helper function to build SQL query with WHERE clauses."""
    where_clauses = []
    params = []
    for key, value in params_dict.copy().items():
        if value:
            actual_key = 'service' if key == 'card_filter_service' else key
            
            if key == 'card_filter_service_type' or actual_key == 'service_type':
                column_name = 'service_type' if key == 'card_filter_service_type' else actual_key
                where_clauses.append(f"{column_name} LIKE %s")
                params.append(f"%{value}%")
            elif key == 'card_filter_lead_type':
                 where_clauses.append(f"lead_type = %s")
                 params.append(value)
            else:
                where_clauses.append(f"{actual_key} = %s")
                params.append(value)
    
    query = base_query
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)
    return query, tuple(params)


@app.route('/')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    now = datetime.datetime.now()
    current_date = now.strftime("%Y년 %m월 %d일") + " " + ["월", "화", "수", "목", "금", "토", "일"][now.weekday()] + "요일"

    card_data = [
        {"id": "company_search", "icon": "fa-building", "title": "업체 정보 조회", "description": "몰아이디 EC 데이터 자동 조회"},
        {"id": "competitor_info", "icon": "fa-search", "title": "카테고리 경쟁사 조회", "description": "몰아이디 EC 데이터 조회"},
        {"id": "coaching_account", "icon": "fa-user-cog", "title": "코칭 계정 관리", "description": "코칭 계정 정보 및 이력 확인"},
        {"id": "team_report", "icon": "fa-chart-bar", "title": "팀보고 리포트", "description": "팀보고 관련 자료 모음"},
        {"id": "sales_db", "icon": "fa-database", "title": "영업DB 관리", "description": "엔터프라이즈 영업 DB 관리"},
        {"id": "schedule", "icon": "fa-calendar-alt", "title": "일정 관리", "description": "미팅 및 주요 일정 현황 관리"}
    ]

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        sql = "SELECT item_id, item_value FROM dashboard_summary"
        cursor.execute(sql)
        db_results = cursor.fetchall()
        db_data_map = {item['item_id']: item['item_value'] for item in db_results}
        
        cursor.execute("SELECT COUNT(*) AS total_leads FROM eco1_sales_leads")
        total_leads_result = cursor.fetchone()
        
        cursor.execute("SELECT COUNT(*) AS confirmed_leads FROM eco1_sales_leads WHERE service = '확정'")
        confirmed_leads_result = cursor.fetchone()
        
        for card in card_data:
            if card['id'] in db_data_map:
                card['value'] = db_data_map[card['id']]
            
            if card['id'] == 'sales_db':
                card['total_leads'] = total_leads_result['total_leads'] if total_leads_result else 0
                card['confirmed_leads'] = confirmed_leads_result['confirmed_leads'] if confirmed_leads_result else 0

    except Exception as e:
        print(f"데이터베이스 오류: {e}")
        for card in card_data:
            if card['id'] == 'sales_db':
                card['total_leads'] = 'Error'
                card['confirmed_leads'] = 'Error'
            elif 'value' not in card:
                card['value'] = 'Error'
    finally:
        if conn:
            conn.close()

    user_name = ALLOWED_USERS.get(session['user_id'])
    return render_template('index.html', cards=card_data, date=current_date, user_name=user_name)

def get_summary_data(leads):
    summary = {
        'sales_status': {'total': 0, 'counts': defaultdict(int), 'formatted_counts': {}, 'percentages': {}},
        'onboarding_status': {'total': 0, 'counts': defaultdict(int), 'formatted_counts': {}, 'percentages': {}},
        'lead_type_status': {'total': 0, 'counts': defaultdict(int), 'formatted_counts': {}, 'percentages': {}}
    }

    total_leads = len(leads)
    
    summary['sales_status']['total'] = total_leads
    summary['lead_type_status']['total'] = total_leads
    status_keys = ['확정', '영업중', '영업전', '실패']
    lead_type_keys = ['C_고객경험강화형', 'C_온보딩집중형', 'O_데이터기반형', 'O_소통강화형', 'O_자동화추구형', 'S_성장주도형', 'S_효율최적화형']

    confirmed_leads = []
    
    if total_leads > 0:
        for lead in leads:
            status = lead.get('service')
            if status in status_keys:
                summary['sales_status']['counts'][status] += 1
            if status == '확정':
                confirmed_leads.append(lead)
            
            lead_type = lead.get('lead_type')
            if lead_type in lead_type_keys:
                summary['lead_type_status']['counts'][lead_type] += 1

        for status in status_keys:
            count = summary['sales_status']['counts'][status]
            summary['sales_status']['formatted_counts'][status] = f"{count:,}"
            percentage = (count / total_leads * 100) if total_leads > 0 else 0
            summary['sales_status']['percentages'][status] = f"{percentage:.1f}"

        for lead_type in lead_type_keys:
            count = summary['lead_type_status']['counts'][lead_type]
            summary['lead_type_status']['formatted_counts'][lead_type] = f"{count:,}"
            percentage = (count / total_leads * 100) if total_leads > 0 else 0
            summary['lead_type_status']['percentages'][lead_type] = f"{percentage:.1f}"

    total_confirmed = len(confirmed_leads)
    summary['onboarding_status']['total'] = total_confirmed
    service_type_keys = ['소통', '기능', '컨설팅']
    if total_confirmed > 0:
        for lead in confirmed_leads:
            service_types = lead.get('service_type', '')
            if service_types:
                types = [t.strip() for t in service_types.split(',')]
                for stype in service_type_keys:
                    if stype in types:
                        summary['onboarding_status']['counts'][stype] += 1
        
        for stype in service_type_keys:
            count = summary['onboarding_status']['counts'][stype]
            summary['onboarding_status']['formatted_counts'][stype] = f"{count:,}"
            percentage = (count / total_confirmed * 100) if total_confirmed > 0 else 0
            summary['onboarding_status']['percentages'][stype] = f"{percentage:.1f}"

    return summary

def clean_and_convert(value):
    if value is None:
        return None
    
    if isinstance(value, decimal.Decimal):
        value = float(value)

    if isinstance(value, str):
        cleaned_str = re.sub(r'[^\d.-]', '', value)
        if cleaned_str and cleaned_str != '.':
            try:
                return float(cleaned_str)
            except ValueError:
                return None
        else:
            return None
    
    if isinstance(value, (int, float)):
        return value
        
    return None

@app.route('/leads')
def leads_list():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    current_tab = request.args.get('tab', '국내', type=str)
    
    search_params = {
        'sorting': request.args.get('sorting', ''),
        'label': request.args.get('label', ''),
        'lead_type': request.args.get('lead_type', ''),
        'manager': request.args.get('manager', ''),
        'service': request.args.get('service', ''),
        'service_type': request.args.get('service_type', ''),
        'onboarding_case': request.args.get('onboarding_case', ''),
        'years': request.args.get('years', ''),
        'mall_id': request.args.get('mall_id', '')
    }
    
    card_filter_service = request.args.get('card_filter_service', '')
    card_filter_service_type = request.args.get('card_filter_service_type', '')
    card_filter_lead_type = request.args.get('card_filter_lead_type', '')

    sort_by = request.args.get('sort_by', 'default')
    sort_order = request.args.get('sort_order', 'desc')


    conn = None
    all_leads_for_table = []
    filter_options = {}
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        summary_search_params = search_params.copy()
        summary_search_params.pop('service', None) 
        summary_search_params.pop('service_type', None)
        summary_search_params.pop('lead_type', None)
        
        summary_query, summary_params = build_query("SELECT * FROM eco1_sales_leads", summary_search_params)
        cursor.execute(summary_query, summary_params)
        all_leads_for_summary = cursor.fetchall()
        
        table_search_params = search_params.copy()
        if card_filter_service:
            table_search_params['service'] = '' 
            table_search_params['card_filter_service'] = card_filter_service

        if card_filter_service_type:
            table_search_params['service_type'] = ''
            table_search_params['card_filter_service_type'] = card_filter_service_type
            table_search_params['service'] = '확정'

        if card_filter_lead_type:
            table_search_params['lead_type'] = ''
            table_search_params['card_filter_lead_type'] = card_filter_lead_type

        table_query, table_params = build_query("SELECT * FROM eco1_sales_leads", table_search_params)
        cursor.execute(table_query, table_params)
        all_leads_for_table = cursor.fetchall()

        options_queries = {
            'sorting': "SELECT DISTINCT sorting FROM eco1_sales_leads WHERE sorting IS NOT NULL AND sorting != '' ORDER BY sorting",
            'label': "SELECT DISTINCT label FROM eco1_sales_leads WHERE label IS NOT NULL AND label != '' ORDER BY label",
            'lead_type': "SELECT DISTINCT lead_type FROM eco1_sales_leads WHERE lead_type IS NOT NULL AND lead_type != '' ORDER BY lead_type",
            'manager': "SELECT DISTINCT manager FROM eco1_sales_leads WHERE manager IS NOT NULL AND manager != '' ORDER BY manager",
            'service': "SELECT DISTINCT service FROM eco1_sales_leads WHERE service IS NOT NULL AND service != '' ORDER BY service",
            'onboarding_case': "SELECT DISTINCT onboarding_case FROM eco1_sales_leads WHERE onboarding_case IS NOT NULL AND onboarding_case != '' ORDER BY onboarding_case",
            'years': """
                SELECT DISTINCT years FROM eco1_sales_leads 
                WHERE years IS NOT NULL AND years != '' AND years NOT LIKE '#%'
                ORDER BY 
                CASE
                    WHEN years = '10년이상' THEN 0 WHEN years = '10년미만' THEN 1 WHEN years = '5년미만' THEN 2
                    WHEN years = '3년미만' THEN 3 WHEN years = '1년미만' THEN 4 ELSE 5
                END
            """
        }
        for name, sql in options_queries.items():
            cursor.execute(sql)
            filter_options[name] = cursor.fetchall()
        
        cursor.execute("SELECT DISTINCT service_type FROM eco1_sales_leads")
        service_types_result = cursor.fetchall()
        unique_service_types = set()
        for row in service_types_result:
            if row['service_type']:
                types = [t.strip() for t in row['service_type'].split(',')]
                unique_service_types.update(types)
        filter_options['service_type'] = sorted(list(unique_service_types))

        for lead in all_leads_for_table:
            if isinstance(lead.get('confirmed_date'), datetime.date) and lead.get('confirmed_date') == datetime.date(1999, 1, 1):
                lead['confirmed_date'] = '미성공'
            
            last_cvr_str = str(lead.get('last_cvr', '0') or '0').strip()
            previous_cvr_str = str(lead.get('previous_cvr', '0') or '0').strip()
            try:
                last_cvr_val = float(last_cvr_str.replace('%',''))
                previous_cvr_val = float(previous_cvr_str.replace('%',''))
                cvr_difference = last_cvr_val - previous_cvr_val
                lead['cvr_change'] = f"{cvr_difference:.2f}"
            except (ValueError, TypeError):
                lead['cvr_change'] = "0.00"
            current_aov_numeric, previous_aov_numeric = 0, 0
            try:
                order_amount = lead.get('last_30_days_order_amount', 0) or 0
                buyer_count = lead.get('last_30_days_buyer_count', 0) or 0
                current_aov_numeric = order_amount / buyer_count if buyer_count > 0 else 0
                lead['aov'] = f"{current_aov_numeric:,.0f}"
            except (TypeError, ValueError, ZeroDivisionError):
                lead['aov'] = "0"
            try:
                prev_order_amount = lead.get('previous_30_days_order_amount', 0) or 0
                prev_buyer_count = lead.get('previous_30_days_buyer_count', 0) or 0
                previous_aov_numeric = prev_order_amount / prev_buyer_count if prev_buyer_count > 0 else 0
            except (TypeError, ValueError, ZeroDivisionError):
                previous_aov_numeric = 0
            try:
                if previous_aov_numeric > 0:
                    growth_rate = ((current_aov_numeric - previous_aov_numeric) / previous_aov_numeric) * 100
                    lead['aov_growth_rate'] = f"{growth_rate:.1f}%"
                else:
                    lead['aov_growth_rate'] = ""
            except (TypeError, ValueError, ZeroDivisionError):
                lead['aov_growth_rate'] = ""

            growth_rate_fields = {
                'order_amount_r': 'order_amount_r_sign', 'all_visit_r': 'all_visit_r_sign',
                'cvr_change': 'cvr_change_sign', 'aov_growth_rate': 'aov_growth_rate_sign',
                'page_view_r': 'page_view_r_sign'
            }
            for field, sign_field in growth_rate_fields.items():
                value_str = str(lead.get(field, ''))
                num_str = re.findall(r'-?\d+\.?\d*', value_str)
                if num_str:
                    try:
                        num = float(num_str[0])
                        if num > 0: lead[sign_field] = 'positive'
                        elif num < 0: lead[sign_field] = 'negative'
                        else: lead[sign_field] = 'neutral'
                    except ValueError: lead[sign_field] = 'neutral'
                else: lead[sign_field] = 'neutral'
        
        sort_map = {
            "order_amount": "last_30_days_order_amount",
            "all_visit": "last_30_days_all_visit",
            "cvr": "last_cvr",
            "aov": "aov",
            "pv": "last_PV",
            "order_amount_r": "order_amount_r",
            "all_visit_r": "all_visit_r",
            "cvr_change": "cvr_change",
            "aov_growth_rate": "aov_growth_rate",
            "page_view_r": "page_view_r"
        }

        sort_by_column = sort_map.get(sort_by)

        if sort_by_column:
            is_reverse = (sort_order == 'desc')
            
            all_leads_for_table.sort(key=lambda lead: (
                clean_and_convert(lead.get(sort_by_column)) is None or clean_and_convert(lead.get(sort_by_column)) == 0,
                clean_and_convert(lead.get(sort_by_column)) is None,
                - (clean_and_convert(lead.get(sort_by_column)) or 0) if is_reverse else (clean_and_convert(lead.get(sort_by_column)) or 0)
            ))
        else:
             all_leads_for_table.sort(key=lambda x: (x.get('service') != '확정', x.get('reg_date')), reverse=False)

        for lead in all_leads_for_table:
            for key in ['last_30_days_all_visit', 'last_30_days_order_amount']:
                 if lead.get(key) is not None and isinstance(lead.get(key), (int, float, decimal.Decimal)):
                    try:
                        lead[key] = f"{int(lead[key]):,}"
                    except (ValueError, TypeError):
                        pass
            try:
                pv_value = float(lead.get('last_PV', 0) or 0)
                lead['last_PV'] = f"{pv_value:.1f}"
            except (ValueError, TypeError):
                pass

    except Exception as e:
        print(f"DB 조회 또는 데이터 가공 오류 (eco1_sales_leads): {e}")
    finally:
        if conn:
            conn.close()
    
    summary_cards_data = get_summary_data(all_leads_for_summary)

    if current_tab == '글로벌':
        filtered_leads = [lead for lead in all_leads_for_table if lead.get('sorting') == '글로벌']
    else:
        filtered_leads = [lead for lead in all_leads_for_table if lead.get('sorting') == '국내']

    total_items = len(filtered_leads)
    total_pages = math.ceil(total_items / per_page) if per_page > 0 else 0
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    paginated_leads = filtered_leads[start_index:end_index]

    now = datetime.datetime.now()
    current_date = now.strftime("%Y년 %m월 %d일") + " " + ["월", "화", "수", "목", "금", "토", "일"][now.weekday()] + "요일"
    
    user_name = ALLOWED_USERS.get(session['user_id'])
    return render_template('leads_list.html', 
                           date=current_date, leads=paginated_leads, current_page=page,
                           total_pages=total_pages, per_page=per_page, current_tab=current_tab,
                           total_items=total_items, filter_options=filter_options,
                           search_params=search_params, summary_cards=summary_cards_data,
                           sort_by=sort_by, sort_order=sort_order, user_name=user_name)

@app.route('/run-workflow', methods=['POST'])
def run_workflow():
    data = request.get_json()
    mall_id = data.get('mall_id')
    n8n_webhook_url = "https://n8n-mi-042-web.hanpda.com/webhook-test/d1f3735d-2f31-491c-be54-63257de0218e"
    
    try:
        response = requests.post(n8n_webhook_url, json={'mall_id': mall_id}, timeout=15)
        response.raise_for_status()
        result_data = response.json()
        return jsonify(result_data)
    except requests.exceptions.RequestException as e:
        print(f"n8n 요청 중 오류: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)