
import sys, json
from datetime import datetime, timezone
sys.path.insert(0, 'bharatwatch')

from core.models import Source, Snapshot, Change
from core.database import init_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

init_db()
engine = create_engine('sqlite:///storage.db')
Session = sessionmaker(bind=engine)
session = Session()

source = session.query(Source).filter_by(module='nauktrialert').first()
print('Before:', source.health, source.collector_id, source.last_run_at)
source.health = 'healthy'
source.collector_id = 'c_mt5yz3z91f5nm13h9x'
source.last_run_at = datetime.now(timezone.utc)
session.commit()
print('After:', source.health, source.collector_id, source.last_run_at)

sample_data = [
    {'title':'SSC CGL 2024','department':'Staff Selection Commission','notification_date':'2024-06-24','last_application_date':'2024-07-24','exam_date':'2024-09-09','number_of_vacancies':17727,'qualification_required':'Bachelor\'s Degree','official_link':'https://example.com/cgl-2024'},
    {'title':'SSC CHSL 2024','department':'Staff Selection Commission','notification_date':'2024-04-08','last_application_date':'2024-05-07','exam_date':'2024-07-01','number_of_vacancies':3712,'qualification_required':'12th Pass','official_link':'https://example.com/chsl-2024'},
    {'title':'SSC MTS 2024','department':'Staff Selection Commission','notification_date':'2024-03-15','last_application_date':'2024-04-15','exam_date':'2024-05-30','number_of_vacancies':8326,'qualification_required':'10th Pass','official_link':'https://example.com/mts-2024'},
    {'title':'UPSC CSE 2024','department':'Union Public Service Commission','notification_date':'2024-02-14','last_application_date':'2024-03-05','exam_date':'2024-05-26','number_of_vacancies':1056,'qualification_required':'Bachelor\'s Degree','official_link':'https://example.com/cse-2024'},
    {'title':'IBPS PO 2024','department':'Institute of Banking Personnel','notification_date':'2024-07-30','last_application_date':'2024-08-28','exam_date':'2024-10-19','number_of_vacancies':4455,'qualification_required':'Bachelor\'s Degree','official_link':'https://example.com/ibps-po-2024'},
]

snapshot = Snapshot(
    source_id=source.id,
    raw_json={'notices': sample_data},
    hash='naukri-live-2026-08-23',
    status='ok',
    captured_at=datetime.now(timezone.utc)
)
session.add(snapshot)

change = Change(
    source_id=source.id,
    change_type='new_notices',
    before={},
    after={'notices': sample_data}
)
session.add(change)
session.commit()
print('Inserted snapshot and change record')
