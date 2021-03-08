from dateutil.relativedelta import relativedelta
from read_db       import ReadDB
from datetime      import datetime, timedelta
from pymongo       import MongoClient
from collections   import OrderedDict

class Return(ReadDB):

    def __init__(self, date, code):
        super().__init__()
        
        self.date_present = datetime.strptime(date, '%Y%m%d')
        self.code = code

        # db의 모든 일자 list: str -> datetime으로 변환
        self.entire_dates = [ datetime.strptime(_date, '%Y%m%d')
            for _date in self.db.Creon['종가'].find().distinct('_id')
        ]

    def closing(self, date):
        return ReadDB.request_info(self, date, self.code, '종가')['value']

    def periodic_returns(self):
        closing_present = self.closing(self.date_present)

        dict_return = OrderedDict()
        for term in ['1주', '2주', '1개월', '3개월', '6개월', '1년']:
            if '주' in term:
                date_past = self.date_present - relativedelta(weeks=int(term.replace('주','')))
            elif '개월' in term:
                date_past = self.date_present - relativedelta(months=int(term.replace('개월','')))
            elif '년' in term:
                date_past = self.date_present - relativedelta(years=int(term.replace('년','')))

            # 영업일이 아닌 경우
            while date_past not in self.entire_dates:
                date_past -= timedelta(1)
            
            # date_past -> str으로 변환
            date_past = datetime.strftime(date_past, '%Y%m%d')
            closing_past = self.closing(date_past)
            dict_return[term+'수익율'] = round(closing_present/closing_past - 1, 4)
        
        return dict_return


X = Return('20210305', 'A030520')
ReadDB.prettify(X.periodic_returns())