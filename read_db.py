from pymongo  import MongoClient
from datetime import datetime
import pprint

class ReadDB:
    def __init__(self):
        self.db = MongoClient("mongodb://<id>:<pwd>@<ip>:<port>")

    @staticmethod
    def prettify(data):
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(data)

    def request_info(self, date, code, item):

        def get_item(date, item):
            if type(date) == datetime:
                date = datetime.strftime(date, '%Y%m%d')

            collection = self.db.Creon[item]
            try:
                return list(collection.find({'_id':date}))[0]
            except IndexError:
                err_msg = "DB에 없는 날짜 혹은 계정입니다."
                raise KeyError(err_msg)

        _dict = get_item(date, item)
        find_dict = next((
            item for item in _dict['items'] if item['code'] == code), -1
        )

        if find_dict == -1:
            raise KeyError("종목코드를 다시 확인하세요.")

        _dict = { 'date' : _dict['_id']}
        _dict.update(find_dict)

        return _dict
