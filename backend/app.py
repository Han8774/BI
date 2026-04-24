"""
Flask后端 - 仙津数据中台
提供四大模块的RESTful API
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DATABASE = 'xianjin_platform.db'

def get_db():
    """获取数据库连接"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """初始化数据库，创建四张表"""
    conn = get_db()
    cursor = conn.cursor()
    
    # 数据资产表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data_assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_code TEXT UNIQUE NOT NULL,
            asset_name TEXT NOT NULL,
            asset_type TEXT,
            department TEXT,
            remark TEXT,
            created_at TEXT DEFAULT (datetime('now', 'localtime'))
        )
    ''')
    
    # 模型结构表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS models (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_code TEXT UNIQUE NOT NULL,
            model_name TEXT NOT NULL,
            model_type TEXT,
            algorithm TEXT,
            owner TEXT,
            description TEXT,
            created_at TEXT DEFAULT (datetime('now', 'localtime'))
        )
    ''')
    
    # 元数据表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meta_name TEXT NOT NULL,
            meta_type TEXT,
            source_system TEXT,
            business_domain TEXT,
            description TEXT,
            created_at TEXT DEFAULT (datetime('now', 'localtime'))
        )
    ''')
    
    # 报表表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_name TEXT NOT NULL,
            report_type TEXT,
            creator TEXT,
            status TEXT DEFAULT '草稿',
            description TEXT,
            created_at TEXT DEFAULT (datetime('now', 'localtime')),
            updated_at TEXT DEFAULT (datetime('now', 'localtime'))
        )
    ''')
    
    conn.commit()
    conn.close()

def row_to_dict(row):
    """将sqlite Row转换为字典"""
    return dict(row) if row else None

# ========== 数据资产 API ==========

@app.route('/api/assets', methods=['GET'])
def get_assets():
    """获取资产列表，支持搜索"""
    conn = get_db()
    cursor = conn.cursor()
    
    search = request.args.get('search', '')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    offset = (page - 1) * page_size
    
    if search:
        cursor.execute('''
            SELECT * FROM data_assets 
            WHERE asset_name LIKE ? OR asset_type LIKE ?
            ORDER BY id DESC LIMIT ? OFFSET ?
        ''', (f'%{search}%', f'%{search}%', page_size, offset))
        cursor.execute('''
            SELECT COUNT(*) FROM data_assets 
            WHERE asset_name LIKE ? OR asset_type LIKE ?
        ''', (f'%{search}%', f'%{search}%'))
    else:
        cursor.execute('SELECT * FROM data_assets ORDER BY id DESC LIMIT ? OFFSET ?', (page_size, offset))
        cursor.execute('SELECT COUNT(*) FROM data_assets')
    
    items = [row_to_dict(row) for row in cursor.fetchall()]
    total = cursor.fetchone()[0]
    conn.close()
    
    return jsonify({'code': 200, 'message': 'success', 'data': {'items': items, 'total': total}})

@app.route('/api/assets', methods=['POST'])
def create_asset():
    """创建资产"""
    data = request.json
    
    if not data.get('asset_code') or not data.get('asset_name'):
        return jsonify({'code': 400, 'message': '资产编号和名称不能为空', 'data': None})
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO data_assets (asset_code, asset_name, asset_type, department, remark)
            VALUES (?, ?, ?, ?, ?)
        ''', (data['asset_code'], data['asset_name'], data.get('asset_type', ''),
              data.get('department', ''), data.get('remark', '')))
        conn.commit()
        asset_id = cursor.lastrowid
        cursor.execute('SELECT * FROM data_assets WHERE id = ?', (asset_id,))
        result = row_to_dict(cursor.fetchone())
        conn.close()
        return jsonify({'code': 200, 'message': '创建成功', 'data': result})
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'code': 400, 'message': '资产编号已存在', 'data': None})

@app.route('/api/assets/<int:id>', methods=['GET'])
def get_asset(id):
    """获取资产详情"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM data_assets WHERE id = ?', (id,))
    result = row_to_dict(cursor.fetchone())
    conn.close()
    
    if result:
        return jsonify({'code': 200, 'message': 'success', 'data': result})
    return jsonify({'code': 404, 'message': '资产不存在', 'data': None})

@app.route('/api/assets/<int:id>', methods=['PUT'])
def update_asset(id):
    """更新资产"""
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE data_assets 
        SET asset_code = ?, asset_name = ?, asset_type = ?, department = ?, remark = ?
        WHERE id = ?
    ''', (data['asset_code'], data['asset_name'], data.get('asset_type', ''),
          data.get('department', ''), data.get('remark', ''), id))
    conn.commit()
    
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'code': 404, 'message': '资产不存在', 'data': None})
    
    cursor.execute('SELECT * FROM data_assets WHERE id = ?', (id,))
    result = row_to_dict(cursor.fetchone())
    conn.close()
    return jsonify({'code': 200, 'message': '更新成功', 'data': result})

@app.route('/api/assets/<int:id>', methods=['DELETE'])
def delete_asset(id):
    """删除资产"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM data_assets WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    if cursor.rowcount > 0:
        return jsonify({'code': 200, 'message': '删除成功', 'data': None})
    return jsonify({'code': 404, 'message': '资产不存在', 'data': None})

# ========== 模型管理 API ==========

@app.route('/api/models', methods=['GET'])
def get_models():
    """获取模型列表"""
    conn = get_db()
    cursor = conn.cursor()
    
    search = request.args.get('search', '')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    offset = (page - 1) * page_size
    
    if search:
        cursor.execute('''
            SELECT * FROM models 
            WHERE model_name LIKE ? OR model_type LIKE ?
            ORDER BY id DESC LIMIT ? OFFSET ?
        ''', (f'%{search}%', f'%{search}%', page_size, offset))
        cursor.execute('''
            SELECT COUNT(*) FROM models 
            WHERE model_name LIKE ? OR model_type LIKE ?
        ''', (f'%{search}%', f'%{search}%'))
    else:
        cursor.execute('SELECT * FROM models ORDER BY id DESC LIMIT ? OFFSET ?', (page_size, offset))
        cursor.execute('SELECT COUNT(*) FROM models')
    
    items = [row_to_dict(row) for row in cursor.fetchall()]
    total = cursor.fetchone()[0]
    conn.close()
    
    return jsonify({'code': 200, 'message': 'success', 'data': {'items': items, 'total': total}})

@app.route('/api/models', methods=['POST'])
def create_model():
    """创建模型"""
    data = request.json
    
    if not data.get('model_code') or not data.get('model_name'):
        return jsonify({'code': 400, 'message': '模型编码和名称不能为空', 'data': None})
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO models (model_code, model_name, model_type, algorithm, owner, description)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data['model_code'], data['model_name'], data.get('model_type', ''),
              data.get('algorithm', ''), data.get('owner', ''), data.get('description', '')))
        conn.commit()
        model_id = cursor.lastrowid
        cursor.execute('SELECT * FROM models WHERE id = ?', (model_id,))
        result = row_to_dict(cursor.fetchone())
        conn.close()
        return jsonify({'code': 200, 'message': '创建成功', 'data': result})
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'code': 400, 'message': '模型编码已存在', 'data': None})

@app.route('/api/models/<int:id>', methods=['GET'])
def get_model(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM models WHERE id = ?', (id,))
    result = row_to_dict(cursor.fetchone())
    conn.close()
    return jsonify({'code': 200, 'message': 'success', 'data': result}) if result else jsonify({'code': 404, 'message': '模型不存在', 'data': None})

@app.route('/api/models/<int:id>', methods=['PUT'])
def update_model(id):
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE models SET model_code = ?, model_name = ?, model_type = ?, algorithm = ?, owner = ?, description = ?
        WHERE id = ?
    ''', (data['model_code'], data['model_name'], data.get('model_type', ''),
          data.get('algorithm', ''), data.get('owner', ''), data.get('description', ''), id))
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'code': 404, 'message': '模型不存在', 'data': None})
    cursor.execute('SELECT * FROM models WHERE id = ?', (id,))
    result = row_to_dict(cursor.fetchone())
    conn.close()
    return jsonify({'code': 200, 'message': '更新成功', 'data': result})

@app.route('/api/models/<int:id>', methods=['DELETE'])
def delete_model(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM models WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'code': 200, 'message': '删除成功', 'data': None}) if cursor.rowcount > 0 else jsonify({'code': 404, 'message': '模型不存在', 'data': None})

# ========== 元数据管理 API ==========

@app.route('/api/metadata', methods=['GET'])
def get_metadata():
    """获取元数据列表"""
    conn = get_db()
    cursor = conn.cursor()
    
    meta_type = request.args.get('meta_type', '')
    business_domain = request.args.get('business_domain', '')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    offset = (page - 1) * page_size
    
    query = 'SELECT * FROM metadata WHERE 1=1'
    params = []
    
    if meta_type:
        query += ' AND meta_type = ?'
        params.append(meta_type)
    if business_domain:
        query += ' AND business_domain LIKE ?'
        params.append(f'%{business_domain}%')
    
    cursor.execute(query + ' ORDER BY id DESC LIMIT ? OFFSET ?', (*params, page_size, offset))
    items = [row_to_dict(row) for row in cursor.fetchall()]
    
    count_query = 'SELECT COUNT(*) FROM metadata WHERE 1=1' + (' AND meta_type = ?' if meta_type else '') + (' AND business_domain LIKE ?' if business_domain else '')
    cursor.execute(count_query, params)
    total = cursor.fetchone()[0]
    conn.close()
    
    return jsonify({'code': 200, 'message': 'success', 'data': {'items': items, 'total': total}})

@app.route('/api/metadata', methods=['POST'])
def create_metadata():
    data = request.json
    if not data.get('meta_name'):
        return jsonify({'code': 400, 'message': '元数据名称不能为空', 'data': None})
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO metadata (meta_name, meta_type, source_system, business_domain, description)
        VALUES (?, ?, ?, ?, ?)
    ''', (data['meta_name'], data.get('meta_type', ''), data.get('source_system', ''),
          data.get('business_domain', ''), data.get('description', '')))
    conn.commit()
    meta_id = cursor.lastrowid
    cursor.execute('SELECT * FROM metadata WHERE id = ?', (meta_id,))
    result = row_to_dict(cursor.fetchone())
    conn.close()
    return jsonify({'code': 200, 'message': '创建成功', 'data': result})

@app.route('/api/metadata/<int:id>', methods=['GET'])
def get_meta(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM metadata WHERE id = ?', (id,))
    result = row_to_dict(cursor.fetchone())
    conn.close()
    return jsonify({'code': 200, 'message': 'success', 'data': result}) if result else jsonify({'code': 404, 'message': '元数据不存在', 'data': None})

@app.route('/api/metadata/<int:id>', methods=['PUT'])
def update_metadata(id):
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE metadata SET meta_name = ?, meta_type = ?, source_system = ?, business_domain = ?, description = ?
        WHERE id = ?
    ''', (data['meta_name'], data.get('meta_type', ''), data.get('source_system', ''),
          data.get('business_domain', ''), data.get('description', ''), id))
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'code': 404, 'message': '元数据不存在', 'data': None})
    cursor.execute('SELECT * FROM metadata WHERE id = ?', (id,))
    result = row_to_dict(cursor.fetchone())
    conn.close()
    return jsonify({'code': 200, 'message': '更新成功', 'data': result})

@app.route('/api/metadata/<int:id>', methods=['DELETE'])
def delete_metadata(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM metadata WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'code': 200, 'message': '删除成功', 'data': None}) if cursor.rowcount > 0 else jsonify({'code': 404, 'message': '元数据不存在', 'data': None})

# ========== 报表管理 API ==========

@app.route('/api/reports', methods=['GET'])
def get_reports():
    """获取报表列表"""
    conn = get_db()
    cursor = conn.cursor()
    
    report_type = request.args.get('report_type', '')
    status = request.args.get('status', '')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    offset = (page - 1) * page_size
    
    query = 'SELECT * FROM reports WHERE 1=1'
    params = []
    
    if report_type:
        query += ' AND report_type = ?'
        params.append(report_type)
    if status:
        query += ' AND status = ?'
        params.append(status)
    
    cursor.execute(query + ' ORDER BY id DESC LIMIT ? OFFSET ?', (*params, page_size, offset))
    items = [row_to_dict(row) for row in cursor.fetchall()]
    
    count_query = 'SELECT COUNT(*) FROM reports WHERE 1=1' + (' AND report_type = ?' if report_type else '') + (' AND status = ?' if status else '')
    cursor.execute(count_query, params)
    total = cursor.fetchone()[0]
    conn.close()
    
    return jsonify({'code': 200, 'message': 'success', 'data': {'items': items, 'total': total}})

@app.route('/api/reports', methods=['POST'])
def create_report():
    data = request.json
    if not data.get('report_name'):
        return jsonify({'code': 400, 'message': '报表名称不能为空', 'data': None})
    
    conn = get_db()
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute('''
        INSERT INTO reports (report_name, report_type, creator, status, description, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (data['report_name'], data.get('report_type', ''), data.get('creator', ''),
          data.get('status', '草稿'), data.get('description', ''), now, now))
    conn.commit()
    report_id = cursor.lastrowid
    cursor.execute('SELECT * FROM reports WHERE id = ?', (report_id,))
    result = row_to_dict(cursor.fetchone())
    conn.close()
    return jsonify({'code': 200, 'message': '创建成功', 'data': result})

@app.route('/api/reports/<int:id>', methods=['GET'])
def get_report(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM reports WHERE id = ?', (id,))
    result = row_to_dict(cursor.fetchone())
    conn.close()
    return jsonify({'code': 200, 'message': 'success', 'data': result}) if result else jsonify({'code': 404, 'message': '报表不存在', 'data': None})

@app.route('/api/reports/<int:id>', methods=['PUT'])
def update_report(id):
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute('''
        UPDATE reports SET report_name = ?, report_type = ?, creator = ?, status = ?, description = ?, updated_at = ?
        WHERE id = ?
    ''', (data['report_name'], data.get('report_type', ''), data.get('creator', ''),
          data.get('status', '草稿'), data.get('description', ''), now, id))
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'code': 404, 'message': '报表不存在', 'data': None})
    cursor.execute('SELECT * FROM reports WHERE id = ?', (id,))
    result = row_to_dict(cursor.fetchone())
    conn.close()
    return jsonify({'code': 200, 'message': '更新成功', 'data': result})

@app.route('/api/reports/<int:id>', methods=['DELETE'])
def delete_report(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM reports WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'code': 200, 'message': '删除成功', 'data': None}) if cursor.rowcount > 0 else jsonify({'code': 404, 'message': '报表不存在', 'data': None})

if __name__ == '__main__':
    init_db()
    print('数据库初始化完成')
    app.run(host='0.0.0.0', port=5000, debug=True)
