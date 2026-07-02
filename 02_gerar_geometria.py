# -*- coding: utf-8 -*-
"""
02_gerar_geometria.py
Gera geo_multi.json (níveis UF, macrorregião e região de saúde) para o painel.
Entradas:
  shp/regiao.shp + .dbf                (view_tb_regiao_saudePolygon - SIRGAS 2000)
  shp/macro.shp + .dbf + .shx          (view_tb_macro_regiao - traz o CÓD MRS)
  macrorregioes_brasil.geojson         (geometria atualizada das macros, MG 2024+)
Saída: geo_multi.json
Dependências: pip install pyshp shapely
"""
import shapefile, json, math
from shapely.geometry import shape, mapping, MultiPolygon
from shapely.ops import unary_union

UF_COD = {11:'RO',12:'AC',13:'AM',14:'RR',15:'PA',16:'AP',17:'TO',21:'MA',22:'PI',23:'CE',
24:'RN',25:'PB',26:'PE',27:'AL',28:'SE',29:'BA',31:'MG',32:'ES',33:'RJ',35:'SP',
41:'PR',42:'SC',43:'RS',50:'MS',51:'MT',52:'GO',53:'DF'}

# ---- projeção plate carrée no canvas 900 x 785.9 (bbox continental do Brasil)
LON0, LAT0, LON1, LAT1 = -73.98557, -33.750772, -29.299584, 5.268534
W = 900.0
SX = W/(LON1-LON0)
H = (LAT1-LAT0)*SX
def proj(lon, lat): return ((lon-LON0)*SX, (LAT1-lat)*SX)

def to_path(geom, tol, prec=1):
    """Simplifica e converte para path SVG, descartando anéis minúsculos."""
    g = geom.simplify(tol, preserve_topology=True)
    gj = mapping(g)
    polys = gj['coordinates'] if gj['type']=='MultiPolygon' else [gj['coordinates']]
    d = []
    for poly in polys:
        for ring in poly:
            pts = [proj(x,y) for x,y in ring]
            if len(pts) < 4: continue
            xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
            if (max(xs)-min(xs))<1.2 and (max(ys)-min(ys))<1.2: continue
            d.append('M'+'L'.join(f'{x:.{prec}f},{y:.{prec}f}' for x,y in pts)+'Z')
    return ''.join(d)

def rep(geom):
    p = geom.representative_point(); return proj(p.x, p.y)

# ---- regiões de saúde (fonte dos códigos e do dissolve das UFs)
sf = shapefile.Reader(shp=open('shp/regiao.shp','rb'), dbf=open('shp/regiao.dbf','rb'))
campos = [f[0] for f in sf.fields[1:]]
rs_feats = []
for sr in sf.iterShapeRecords():
    rec = dict(zip(campos, sr.record))
    rs_feats.append({'cod': int(rec['co_regiao_']), 'nome': rec['no_regiao0'],
                     'geom': shape(sr.shape.__geo_interface__).buffer(0)})

# ---- UFs por dissolve
from collections import defaultdict
por_uf = defaultdict(list)
for f in rs_feats: por_uf[UF_COD[f['cod']//1000]].append(f['geom'])
uf_feats = [{'cod':k,'nome':k,'geom':unary_union(v)} for k,v in por_uf.items()]

# ---- macros: código do dbf + geometria atualizada do GeoJSON, casadas pela etiqueta
sfm = shapefile.Reader(shp=open('shp/macro.shp','rb'), dbf=open('shp/macro.dbf','rb'),
                       shx=open('shp/macro.shx','rb'))
cm = [f[0] for f in sfm.fields[1:]]
et2cod = {dict(zip(cm,sr.record))['Etiqueta']: int(dict(zip(cm,sr.record))['Código'])
          for sr in sfm.iterShapeRecords()}
gj = json.load(open('macrorregioes_brasil.geojson', encoding='utf-8'))
m_feats = [{'cod': et2cod[f['properties']['ETIQUETA']], 'nome': f['properties']['ETIQUETA'],
            'geom': shape(f['geometry']).buffer(0)} for f in gj['features']]

def montar(feats, tol):
    out=[]
    for f in feats:
        d = to_path(f['geom'], tol)
        if not d: continue
        cx, cy = rep(f['geom'])
        out.append({'id':f['cod'],'nome':f['nome'],'d':d,'cx':round(cx,1),'cy':round(cy,1)})
    return out

niveis = {'uf':montar(uf_feats,0.030), 'macro':montar(m_feats,0.022), 'rs':montar(rs_feats,0.016)}

# ---- bounding box de zoom por UF, excluindo ilhas oceânicas remotas
#      (Trindade/Martim Vaz no ES, F. de Noronha em PE)
bb = {}
for f in uf_feats:
    g = f['geom']
    polys = list(g.geoms) if isinstance(g, MultiPolygon) else [g]
    principal = max(polys, key=lambda p: p.area)
    cx, cy = principal.centroid.x, principal.centroid.y
    mantidas = [p for p in polys if p.area >= principal.area*0.01
                or math.hypot(p.centroid.x-cx, p.centroid.y-cy) < 3.0]
    b = unary_union(mantidas).bounds
    x0,y1 = proj(b[0],b[1]); x1,y0 = proj(b[2],b[3])
    bb[f['cod']] = [round(x0,1),round(y0,1),round(x1,1),round(y1,1)]

# ---- raio dos alvos de toque por UF (não invadir o rótulo vizinho)
pts = {t['id']:(t['cx'],t['cy']) for t in niveis['uf']}
for t in niveis['uf']:
    t['bb'] = bb[t['id']]
    ax,ay = pts[t['id']]
    dmin = min(math.hypot(ax-bx,ay-by) for k,(bx,by) in pts.items() if k!=t['id'])
    t['r'] = round(min(16, dmin*0.45), 1)

borda = ''.join(to_path(f['geom'], 0.030) for f in uf_feats)
geo = {'W':W, 'H':round(H,1), 'niveis':niveis, 'bordaUF':borda}
json.dump(geo, open('geo_multi.json','w',encoding='utf-8'), ensure_ascii=False, separators=(',',':'))
print(f"geo_multi.json: {len(niveis['uf'])} UFs, {len(niveis['macro'])} macros, {len(niveis['rs'])} regiões")
