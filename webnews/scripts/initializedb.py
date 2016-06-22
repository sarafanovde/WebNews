import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )
from ..models.mymodel import News, User


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = get_engine(settings)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
        news1 = News(Topic = 'iPhone 7 поступил в массовое производство', ShortInfo = 'До предполагаемого релиза Apple iPhone 7 остается 3 месяца и, по слухам, компания уже разместила заказ на производство 78 миллионов смартфонов. Заказ был разделен, по меньшей мере, между двумя крупными производственными компаниями: Foxconn и Pegatron. Последний, как свидетельствуют инсайдеры, на днях приступил к производству первых iPhone 7, который попадут на рынок. Как утверждает OnLeaks, Pegatron будет отвечать за продукцию только 4,7-дюймовых моделей, тогда как 5,5-дюймовый iPhone 7 Plus сойдет с конвейера Foxconn.', Data = 'До предполагаемого релиза Apple iPhone 7 остается 3 месяца и, по слухам, компания уже разместила заказ на производство 78 миллионов смартфонов. Заказ был разделен, по меньшей мере, между двумя крупными производственными компаниями: Foxconn и Pegatron. Последний, как свидетельствуют инсайдеры, на днях приступил к производству первых iPhone 7, который попадут на рынок. Как утверждает OnLeaks, Pegatron будет отвечать за продукцию только 4,7-дюймовых моделей, тогда как 5,5-дюймовый iPhone 7 Plus сойдет с конвейера Foxconn. Как показывает опыт минувших лет, вслед за подобными новостями количество реальных утечек возрастает многократно, а значит, уже скоро мы получим первые подтверждения или опровержения разных слухов, что сейчас ходят в сети. Например, утверждается, что в целом дизайн смартфонов останется прежним, однако исчезнет 3,5-мм аудиовыход, сместятся к верхнему и нижнему краю полоски антенн, возможно, уменьшатся рамки вокруг дисплея. Более смелые предположения говорят о появлении в линейке нового цвета - ярко-синего взамен темно-серого. В 4,7-дюймовом аппарате по-прежнему будет установлена единственная основная камера, тогда как в iPhone 7 Plus может появиться дублирующий модуль для повышения качества снимков. С другой стороны, по последней информации технические проблемы могут заставить Apple отказаться от двойной камеры и старшая версия в этом году тоже выйдет в прежней комплектации. Оба смартфона будут работать на базе процессора Apple A10, получат iOS 10 "из коробки" и, возможно, увеличенный объем оперативной памяти.', image_name = '1.jpg')
        user = User(Name='admin', Age=20, Password = '50300118')
        user1= User(Name='root', Age=20, Password = '123')
        news2 = News(Topic = 'В Windows 10 можно будет работать с одним приложением на разных устройствах', ShortInfo = 'В апреле этого года появилась информация, что Microsoft собирается реализовать в Windows 10 аналог функции Handoff из OS X и iOS. Напомним, что с её помощью пользователи могут отвечать на входящие звонки и сообщения с любого устройства, а также начать работать в приложении, например, на iPhone или iPad, а затем продолжить с того же места на Mac. В последней тестовой сборке Windows 10 Mobile в настройках появилась опция Continue App Experiences, которая предлагает пользователям те же самые возможности, что и Handoff.', Data = 'В апреле этого года появилась информация, что Microsoft собирается реализовать в Windows 10 аналог функции Handoff из OS X и iOS. Напомним, что с её помощью пользователи могут отвечать на входящие звонки и сообщения с любого устройства, а также начать работать в приложении, например, на iPhone или iPad, а затем продолжить с того же места на Mac. В последней тестовой сборке Windows 10 Mobile в настройках появилась опция Continue App Experiences, которая предлагает пользователям те же самые возможности, что и Handoff. Стоит отметить, что на данный момент речь идёт лишь о продолжении работы в приложениях на разных устройствах под управлением Windows 10. Но ранее в этом году на конференции для разработчиков Build 2016 компания Microsoft показала скриншот, где с компьютера отвечают на входящий звонок, который поступает на телефон.', image_name = '1.jpg')
        dbsession.add(news1)
        dbsession.add(news2)
        dbsession.add(user)
        dbsession.add(user1)
