import random
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session

from ..models import User, Bean, Recipe, Article, Gear, GearReview
from ..models.gear import GearType
from ..utils.auth import get_password_hash
from ..core.logging import get_logger

logger = get_logger("seed_factory")


class SeedFactory:
    def __init__(self, db: Session):
        self.db = db

    def seed_all(self) -> dict:
        existing = self.db.query(User).filter(User.username == "barista_kim").first()
        if existing:
            return {"status": "already_seeded"}

        logger.info("Starting full database seed...")
        users = self._create_users()
        beans = self._create_beans(users)
        recipes = self._create_recipes(users, beans)
        articles = self._create_articles(users)
        gears = self._create_gears()
        reviews = self._create_gear_reviews(users, gears)

        return {
            "status": "seeded",
            "users": len(users),
            "beans": len(beans),
            "recipes": len(recipes),
            "articles": len(articles),
            "gears": len(gears),
            "reviews": len(reviews),
        }

    def _create_users(self):
        user_data = [
            {"username": "barista_kim", "email": "kim@beandebug.com", "full_name": "김바리스타", "bio": "10년차 바리스타, 스페셜티 커피 마니아"},
            {"username": "coffee_lee", "email": "lee@beandebug.com", "full_name": "이커피", "bio": "홈카페 마스터, V60 전문가"},
            {"username": "roaster_park", "email": "park@beandebug.com", "full_name": "박로스터", "bio": "커피 로스팅 & 커핑 전문가"},
            {"username": "brew_choi", "email": "choi@beandebug.com", "full_name": "최브루", "bio": "에어로프레스 챔피언십 참가자"},
            {"username": "cafe_jung", "email": "jung@beandebug.com", "full_name": "정카페", "bio": "카페 운영자, 라떼아트 마스터"},
        ]
        users = []
        for i, data in enumerate(user_data):
            u = User(
                **data,
                hashed_password=get_password_hash("password123"),
                is_active=True,
                is_admin=(i == 0),
            )
            self.db.add(u)
            users.append(u)
        self.db.commit()
        for u in users:
            self.db.refresh(u)
        return users

    def _create_beans(self, users):
        bean_catalog = [
            {"name": "예가체프 코체레", "origin": "Ethiopia", "farm": "Kochere Cooperative", "variety": "Heirloom", "roast_level": "light", "processing": "Washed", "altitude": "1,800-2,200m", "flavor_notes": "Floral, Citrus, Tea-like, Bergamot", "tasting_notes": "밝은 산미와 꽃향이 인상적인 클래식 예가체프", "price": 28000, "vendor": "Coffee Lab"},
            {"name": "콜롬비아 수프리모 우일라", "origin": "Colombia", "farm": "Finca El Paraiso", "variety": "Caturra", "roast_level": "medium", "processing": "Washed", "altitude": "1,500-1,800m", "flavor_notes": "Chocolate, Caramel, Nutty, Red Apple", "tasting_notes": "깔끔한 바디와 초콜릿 향이 매력적", "price": 22000, "vendor": "Bean Bros"},
            {"name": "케냐 AA 니에리", "origin": "Kenya", "farm": "Nyeri Hill Estate", "variety": "SL28", "roast_level": "light", "processing": "Washed", "altitude": "1,700-2,000m", "flavor_notes": "Blackcurrant, Grapefruit, Wine, Tomato", "tasting_notes": "강렬한 과일 산미와 와인 같은 바디감", "price": 32000, "vendor": "Artisan Roasters"},
            {"name": "브라질 세하도", "origin": "Brazil", "farm": "Fazenda Santa Lucia", "variety": "Bourbon", "roast_level": "medium", "processing": "Natural", "altitude": "1,100-1,300m", "flavor_notes": "Chocolate, Hazelnut, Brown Sugar, Low Acidity", "tasting_notes": "부드럽고 고소한 견과류 풍미의 기본에 충실한 원두", "price": 18000, "vendor": "Coffee Lab"},
            {"name": "과테말라 안티구아", "origin": "Guatemala", "farm": "Finca La Hermosa", "variety": "Bourbon", "roast_level": "medium", "processing": "Washed", "altitude": "1,500-1,700m", "flavor_notes": "Cocoa, Spice, Orange, Smoky", "tasting_notes": "스모키한 향과 스파이시한 풍미가 독특", "price": 25000, "vendor": "Roast House"},
            {"name": "코스타리카 타라주", "origin": "Costa Rica", "farm": "Hacienda Sonora", "variety": "Villa Sarchi", "roast_level": "light", "processing": "Honey", "altitude": "1,200-1,700m", "flavor_notes": "Honey, Peach, Vanilla, Bright Acidity", "tasting_notes": "허니 프로세스 특유의 달콤하고 과일향 풍부한 맛", "price": 27000, "vendor": "Bean Bros"},
            {"name": "파나마 게이샤", "origin": "Panama", "farm": "Finca La Esmeralda", "variety": "Geisha", "roast_level": "light", "processing": "Washed", "altitude": "1,600-1,800m", "flavor_notes": "Jasmine, Tropical Fruit, Bergamot, Silky", "tasting_notes": "커피의 꽃, 재스민 향과 열대과일의 환상적인 조합", "price": 85000, "vendor": "Artisan Roasters"},
            {"name": "르완다 킹보", "origin": "Rwanda", "farm": "Kingbo Washing Station", "variety": "Red Bourbon", "roast_level": "light", "processing": "Washed", "altitude": "1,700-2,000m", "flavor_notes": "Raspberry, Lemon, Black Tea, Floral", "tasting_notes": "라즈베리 같은 밝은 과일 산미가 매력적", "price": 26000, "vendor": "Coffee Lab"},
            {"name": "인도네시아 만델링", "origin": "Indonesia", "farm": "Lintong Region", "variety": "Typica", "roast_level": "dark", "processing": "Wet-hulled", "altitude": "1,200-1,500m", "flavor_notes": "Earthy, Herbal, Dark Chocolate, Full Body", "tasting_notes": "묵직한 바디감과 허벌, 다크 초콜릿 풍미", "price": 20000, "vendor": "Roast House"},
            {"name": "에티오피아 시다모 내추럴", "origin": "Ethiopia", "farm": "Bensa District", "variety": "Heirloom", "roast_level": "light", "processing": "Natural", "altitude": "1,900-2,100m", "flavor_notes": "Blueberry, Strawberry, Wine, Sweet", "tasting_notes": "블루베리 폭탄! 내추럴 프로세스의 진수", "price": 30000, "vendor": "Artisan Roasters"},
            {"name": "콜롬비아 나리뇨", "origin": "Colombia", "farm": "San Lorenzo", "variety": "Castillo", "roast_level": "medium", "processing": "Washed", "altitude": "1,800-2,200m", "flavor_notes": "Green Apple, Citrus, Panela, Creamy", "tasting_notes": "사과 같은 산미와 파넬라 당의 단맛 밸런스", "price": 24000, "vendor": "Bean Bros"},
            {"name": "에티오피아 구지 우라가", "origin": "Ethiopia", "farm": "Uraga Cooperative", "variety": "Heirloom", "roast_level": "light", "processing": "Natural", "altitude": "2,000-2,200m", "flavor_notes": "Mango, Peach, Floral, Winey", "tasting_notes": "망고와 복숭아 과일 풍미가 가득한 내추럴", "price": 29000, "vendor": "Coffee Lab"},
            {"name": "예멘 모카 마타리", "origin": "Yemen", "farm": "Bani Matar Region", "variety": "Typica", "roast_level": "medium", "processing": "Natural", "altitude": "1,500-2,500m", "flavor_notes": "Wine, Chocolate, Dried Fruit, Spice", "tasting_notes": "와인 같은 바디에 말린 과일과 스파이스 향", "price": 65000, "vendor": "Artisan Roasters"},
            {"name": "하와이 코나", "origin": "Hawaii", "farm": "Greenwell Farms", "variety": "Typica", "roast_level": "medium", "processing": "Washed", "altitude": "600-900m", "flavor_notes": "Butter, Brown Sugar, Mild Acidity, Smooth", "tasting_notes": "버터리한 질감과 부드러운 단맛이 특징", "price": 55000, "vendor": "Roast House"},
            {"name": "자메이카 블루마운틴", "origin": "Jamaica", "farm": "Mavis Bank Estate", "variety": "Typica", "roast_level": "medium", "processing": "Washed", "altitude": "900-1,500m", "flavor_notes": "Balanced, Floral, Nutty, Clean", "tasting_notes": "완벽한 밸런스의 정석, 깨끗한 컵", "price": 90000, "vendor": "Artisan Roasters"},
            {"name": "엘살바도르 파카마라", "origin": "El Salvador", "farm": "Finca Santa Petrona", "variety": "Pacamara", "roast_level": "light", "processing": "Honey", "altitude": "1,500-1,800m", "flavor_notes": "Papaya, Citrus, Honey, Creamy", "tasting_notes": "파카마라 품종 특유의 크리미한 바디감", "price": 35000, "vendor": "Bean Bros"},
            {"name": "탄자니아 킬리만자로", "origin": "Tanzania", "farm": "Kilimanjaro Region", "variety": "Kent", "roast_level": "medium", "processing": "Washed", "altitude": "1,400-1,800m", "flavor_notes": "Black Tea, Lemon, Floral, Bright", "tasting_notes": "밝고 깔끔한 산미에 홍차 같은 우아함", "price": 23000, "vendor": "Roast House"},
            {"name": "페루 찬차마요", "origin": "Peru", "farm": "Junin Region", "variety": "Caturra", "roast_level": "medium", "processing": "Washed", "altitude": "1,200-1,800m", "flavor_notes": "Chocolate, Maple, Citrus, Mild", "tasting_notes": "메이플 시럽 같은 단맛과 마일드한 밸런스", "price": 19000, "vendor": "Coffee Lab"},
            {"name": "멕시코 치아파스", "origin": "Mexico", "farm": "Finca Irlanda", "variety": "Bourbon", "roast_level": "medium", "processing": "Washed", "altitude": "1,000-1,500m", "flavor_notes": "Cocoa, Almond, Cherry, Medium Body", "tasting_notes": "아몬드와 체리 향이 조화로운 미디엄 바디", "price": 17000, "vendor": "Bean Bros"},
            {"name": "에티오피아 게데브 첼바사", "origin": "Ethiopia", "farm": "Chelbesa Washing Station", "variety": "Heirloom", "roast_level": "light", "processing": "Washed", "altitude": "1,900-2,100m", "flavor_notes": "Lemon, Peach, Jasmine, Silky", "tasting_notes": "실키한 마우스필과 레몬, 자스민 향의 조합", "price": 31000, "vendor": "Artisan Roasters"},
            {"name": "니카라과 마타갈파", "origin": "Nicaragua", "farm": "Finca El Limoncillo", "variety": "Java", "roast_level": "medium", "processing": "Natural", "altitude": "1,100-1,400m", "flavor_notes": "Dark Chocolate, Rum, Cherry, Sweet", "tasting_notes": "다크 초콜릿과 럼 같은 달콤한 풍미", "price": 21000, "vendor": "Roast House"},
            {"name": "미얀마 스페셜티", "origin": "Myanmar", "farm": "Shan State", "variety": "Catimor", "roast_level": "medium", "processing": "Washed", "altitude": "1,200-1,500m", "flavor_notes": "Plum, Brown Sugar, Mild, Clean", "tasting_notes": "자두와 흑설탕 풍미의 클린한 컵", "price": 16000, "vendor": "Coffee Lab"},
            {"name": "볼리비아 카라나비", "origin": "Bolivia", "farm": "Caranavi Region", "variety": "Caturra", "roast_level": "light", "processing": "Washed", "altitude": "1,400-1,800m", "flavor_notes": "Red Grape, Floral, Tangerine, Complex", "tasting_notes": "붉은 포도와 탄제린의 복합적인 산미", "price": 33000, "vendor": "Artisan Roasters"},
            {"name": "인도 몬순 말라바", "origin": "India", "farm": "Malabar Coast", "variety": "Kent", "roast_level": "dark", "processing": "Monsooned", "altitude": "900-1,100m", "flavor_notes": "Tobacco, Cedar, Spice, Low Acidity", "tasting_notes": "몬순 프로세스의 독특한 우디, 스파이시 풍미", "price": 22000, "vendor": "Roast House"},
            {"name": "부룬디 카얀자", "origin": "Burundi", "farm": "Kayanza Province", "variety": "Red Bourbon", "roast_level": "light", "processing": "Washed", "altitude": "1,700-2,000m", "flavor_notes": "Orange, Caramel, Floral, Juicy", "tasting_notes": "오렌지 주스 같은 쥬시한 산미가 매력적", "price": 25000, "vendor": "Coffee Lab"},
            {"name": "콩고 키부", "origin": "Congo", "farm": "Lake Kivu Region", "variety": "Bourbon", "roast_level": "medium", "processing": "Washed", "altitude": "1,500-2,000m", "flavor_notes": "Cherry, Dark Chocolate, Tobacco, Rich", "tasting_notes": "체리와 다크 초콜릿의 리치한 조합", "price": 24000, "vendor": "Bean Bros"},
            {"name": "필리핀 바렌시아", "origin": "Philippines", "farm": "Bukidnon Region", "variety": "Liberica", "roast_level": "medium", "processing": "Natural", "altitude": "800-1,200m", "flavor_notes": "Jackfruit, Floral, Woody, Bold", "tasting_notes": "리베리카 특유의 잭프루트와 우디한 향", "price": 28000, "vendor": "Artisan Roasters"},
            {"name": "중국 윈난", "origin": "China", "farm": "Yunnan Province", "variety": "Catimor", "roast_level": "medium", "processing": "Washed", "altitude": "1,100-1,600m", "flavor_notes": "Caramel, Green Tea, Mild Citrus, Smooth", "tasting_notes": "녹차와 캐러멜의 부드러운 조합", "price": 15000, "vendor": "Roast House"},
            {"name": "도미니카 바라오나", "origin": "Dominican Republic", "farm": "Barahona Region", "variety": "Typica", "roast_level": "medium", "processing": "Washed", "altitude": "600-1,200m", "flavor_notes": "Cocoa, Orange Peel, Sweet, Balanced", "tasting_notes": "코코아와 오렌지 필의 스위트한 밸런스", "price": 20000, "vendor": "Coffee Lab"},
            {"name": "우간다 시피 폴스", "origin": "Uganda", "farm": "Sipi Falls Region", "variety": "SL14", "roast_level": "light", "processing": "Natural", "altitude": "1,500-2,000m", "flavor_notes": "Dried Mango, Raspberry, Wine, Complex", "tasting_notes": "건조 망고와 라즈베리의 와이니한 복합 풍미", "price": 23000, "vendor": "Bean Bros"},
        ]

        beans = []
        now = datetime.now(timezone.utc)
        for i, data in enumerate(bean_catalog):
            user = users[i % len(users)]
            bean = Bean(
                **data,
                is_public=True,
                owner_id=user.id,
                created_at=now - timedelta(days=random.randint(1, 90)),
            )
            self.db.add(bean)
            beans.append(bean)
        self.db.commit()
        for b in beans:
            self.db.refresh(b)
        logger.info(f"Created {len(beans)} beans")
        return beans

    def _create_recipes(self, users, beans):
        recipe_templates = [
            {"title": "V60 기본 레시피", "brew_method": "V60", "grind_size": "Medium-Fine", "water_temp": 93, "coffee_amount": 18, "water_amount": 300, "brew_time": 180, "ratio": "1:16.7", "steps": "필터 린싱 → 커피 투입 → 30g 블루밍 30초 → 원형 푸어링 3회 → 2:30 드립 완료", "tips": "물줄기를 일정하게 유지하세요", "description": "깔끔하고 밝은 산미를 즐길 수 있는 기본 V60 추출법"},
            {"title": "V60 아이스 브루잉", "brew_method": "V60", "grind_size": "Medium", "water_temp": 96, "coffee_amount": 22, "water_amount": 200, "brew_time": 150, "ratio": "1:9 + 얼음 130g", "steps": "서버에 얼음 130g → 필터 린싱 → 22g 커피 → 40g 블루밍 → 빠른 푸어링 → 얼음 위 추출", "tips": "뜨거운 물을 얼음 위에 바로 추출해 급냉시키세요", "description": "여름에 즐기는 선명한 산미의 아이스 V60 레시피"},
            {"title": "에어로프레스 인버트", "brew_method": "Aeropress", "grind_size": "Fine-Medium", "water_temp": 85, "coffee_amount": 15, "water_amount": 200, "brew_time": 120, "ratio": "1:13.3", "steps": "인버트 세팅 → 커피 투입 → 85도 물 200g → 1분 스티핑 → 30초 스월 → 플런지 30초", "tips": "너무 강하게 누르지 말고 일정한 압력으로", "description": "풍부한 바디감과 깊은 풍미의 인버트 방식 에어로프레스"},
            {"title": "에어로프레스 바이패스", "brew_method": "Aeropress", "grind_size": "Fine", "water_temp": 90, "coffee_amount": 18, "water_amount": 100, "brew_time": 90, "ratio": "1:5.5 + 바이패스 100ml", "steps": "인버트 → 18g 커피 → 100g 물 → 1분 스티핑 → 플런지 → 뜨거운 물 100ml 바이패스", "tips": "바이패스 물의 양으로 농도를 조절하세요", "description": "바이패스 기법으로 깔끔하면서도 풍부한 맛을 내는 레시피"},
            {"title": "프렌치프레스 클래식", "brew_method": "French Press", "grind_size": "Coarse", "water_temp": 96, "coffee_amount": 30, "water_amount": 500, "brew_time": 240, "ratio": "1:16.7", "steps": "프레스에 커피 투입 → 물 500g 일시 투입 → 4분 스티핑 → 크러스트 제거 → 천천히 플런지", "tips": "크러스트를 스푼으로 걷어내면 더 깔끔한 맛", "description": "묵직한 바디감과 오일리한 질감의 클래식 프렌치프레스"},
            {"title": "콜드브루 12시간", "brew_method": "Cold Brew", "grind_size": "Coarse", "water_temp": 4, "coffee_amount": 100, "water_amount": 1000, "brew_time": 720, "ratio": "1:10", "steps": "굵게 분쇄 → 상온 물 1L에 침지 → 냉장고 12시간 → 필터링 → 원액:물 1:1 희석", "tips": "원액은 냉장 보관 시 2주까지 가능", "description": "부드럽고 달콤한 콜드브루, 여름 필수 레시피"},
            {"title": "콜드브루 급속 18시간", "brew_method": "Cold Brew", "grind_size": "Medium-Coarse", "water_temp": 4, "coffee_amount": 80, "water_amount": 800, "brew_time": 1080, "ratio": "1:10", "steps": "미디엄-코스 분쇄 → 차가운 물 투입 → 냉장 18시간 → 이중 필터링", "tips": "18시간 이상 추출하면 쓴맛이 강해질 수 있어요", "description": "18시간 느린 추출로 더욱 깊은 풍미의 콜드브루"},
            {"title": "모카포트 에스프레소", "brew_method": "Moka Pot", "grind_size": "Fine", "water_temp": 70, "coffee_amount": 20, "water_amount": 250, "brew_time": 300, "ratio": "1:12.5", "steps": "하부 챔버에 뜨거운 물 → 바스켓에 커피 레벨링 → 조립 → 중불 → 추출음 나면 불 끄기", "tips": "미리 데운 물을 사용하면 과추출 방지", "description": "집에서 즐기는 진한 에스프레소 스타일 커피"},
            {"title": "모카포트 라떼", "brew_method": "Moka Pot", "grind_size": "Fine", "water_temp": 70, "coffee_amount": 20, "water_amount": 200, "brew_time": 300, "ratio": "커피:우유 1:3", "steps": "모카포트 추출 → 우유 150ml 스팀/전자렌지 → 우유에 에스프레소 투입 → 시럽 선택 추가", "tips": "우유는 65도 이상 넘기지 마세요", "description": "모카포트로 만드는 부드러운 카페라떼"},
            {"title": "캐맥스 4인분", "brew_method": "Chemex", "grind_size": "Medium-Coarse", "water_temp": 94, "coffee_amount": 42, "water_amount": 700, "brew_time": 270, "ratio": "1:16.7", "steps": "캐맥스 필터 세팅 → 린싱 → 42g 커피 → 80g 블루밍 → 4회 나눠 푸어링 → 4:30 완료", "tips": "캐맥스 두꺼운 필터가 깔끔한 맛의 비결", "description": "깔끔하고 스위트한 캐맥스 레시피"},
            {"title": "사이폰 브루잉", "brew_method": "Siphon", "grind_size": "Medium", "water_temp": 94, "coffee_amount": 25, "water_amount": 360, "brew_time": 90, "ratio": "1:14.4", "steps": "하부에 물 → 가열 → 상부 장착 → 물 올라오면 커피 투입 → 1분 교반 → 불 제거", "tips": "교반은 부드럽게 2-3회만", "description": "사이폰의 극적인 비주얼과 깔끔한 맛"},
            {"title": "터키식 커피", "brew_method": "Turkish", "grind_size": "Extra Fine", "water_temp": 70, "coffee_amount": 10, "water_amount": 100, "brew_time": 180, "ratio": "1:10", "steps": "이브릭에 물+커피+설탕 → 약불 가열 → 거품 올라오면 제거 → 3회 반복 → 잔에 천천히 따르기", "tips": "절대 끓이지 말고 거품이 올라올 때까지만", "description": "천년 역사의 전통 터키식 커피 추출법"},
            {"title": "V60 스위트 포인트", "brew_method": "V60", "grind_size": "Medium-Fine", "water_temp": 90, "coffee_amount": 20, "water_amount": 320, "brew_time": 200, "ratio": "1:16", "steps": "린싱 → 20g 커피 → 40g 블루밍 40초 → 중심 집중 푸어링 → 주변부 한 바퀴 → 드립 완료", "tips": "중심 푸어링으로 스위트니스를 극대화", "description": "단맛을 극대화한 V60 스위트 추출법"},
            {"title": "에어로프레스 에스프레소 스타일", "brew_method": "Aeropress", "grind_size": "Fine", "water_temp": 93, "coffee_amount": 18, "water_amount": 55, "brew_time": 60, "ratio": "1:3", "steps": "인버트 → 미세 분쇄 18g → 93도 물 55g → 10초 스월 → 강한 프레스 30초", "tips": "에스프레소 대체용으로 라떼에 사용 가능", "description": "에어로프레스로 만드는 에스프레소 농도의 커피"},
            {"title": "프렌치프레스 콜드브루", "brew_method": "French Press", "grind_size": "Extra Coarse", "water_temp": 20, "coffee_amount": 60, "water_amount": 450, "brew_time": 720, "ratio": "1:7.5", "steps": "굵게 분쇄 → 상온 물 투입 → 플런저 올린 채 냉장 12시간 → 플런지 → 원액:물 1:1 희석", "tips": "프렌치프레스 메쉬 필터로 쉽게 콜드브루를!", "description": "프렌치프레스를 활용한 간편 콜드브루 레시피"},
            {"title": "V60 46 메서드", "brew_method": "V60", "grind_size": "Medium-Coarse", "water_temp": 93, "coffee_amount": 20, "water_amount": 300, "brew_time": 210, "ratio": "1:15", "steps": "20g 커피 → 60g 1차 주수 45초 → 60g 2차 주수 → 60g 3차 → 60g 4차 → 60g 5차 → 3:30 완료", "tips": "첫 2회 주수가 단맛과 산미를 결정합니다", "description": "4:6 메서드로 맛의 밸런스를 자유롭게 조절하는 레시피"},
            {"title": "클레버 드리퍼", "brew_method": "Clever Dripper", "grind_size": "Medium", "water_temp": 92, "coffee_amount": 18, "water_amount": 270, "brew_time": 210, "ratio": "1:15", "steps": "필터 린싱 → 커피 투입 → 92도 물 270g → 뚜껑 덮고 3분 스티핑 → 서버 위에 올려 드립", "tips": "침지+드립의 장점을 모두 가진 추출기구", "description": "초보자 친화적인 클레버 드리퍼 레시피"},
            {"title": "넬 드립", "brew_method": "Nel Drip", "grind_size": "Medium-Coarse", "water_temp": 88, "coffee_amount": 25, "water_amount": 300, "brew_time": 240, "ratio": "1:12", "steps": "넬 필터 적시기 → 커피 투입 → 뜸들이기 30초 → 가는 물줄기로 천천히 → 3분 30초까지 추출", "tips": "넬 필터는 사용 후 반드시 물에 보관", "description": "오일리하고 부드러운 넬 드립 추출법"},
            {"title": "에어로프레스 챔피언 레시피 2025", "brew_method": "Aeropress", "grind_size": "Medium-Fine", "water_temp": 80, "coffee_amount": 16, "water_amount": 230, "brew_time": 150, "ratio": "1:14.4", "steps": "인버트 → 16g 커피 → 80도 물 230g → 스월 5초 → 2분 스티핑 → 부드럽게 플런지 30초", "tips": "낮은 수온이 클린한 산미의 핵심", "description": "에어로프레스 챔피언십 우승 레시피를 재현"},
            {"title": "모카포트 아메리카노", "brew_method": "Moka Pot", "grind_size": "Fine", "water_temp": 70, "coffee_amount": 18, "water_amount": 150, "brew_time": 240, "ratio": "1:8 + 물 200ml", "steps": "모카포트 추출 → 뜨거운 물 200ml 준비 → 추출 커피를 물에 투입 → 취향에 따라 조절", "tips": "물의 양으로 농도를 자유롭게 조절", "description": "모카포트로 만드는 깔끔한 아메리카노"},
            {"title": "드립백 최적화 레시피", "brew_method": "Drip Bag", "grind_size": "Pre-ground", "water_temp": 90, "coffee_amount": 10, "water_amount": 180, "brew_time": 150, "ratio": "1:18", "steps": "드립백 개봉 → 컵에 걸기 → 90도 물 30g 블루밍 → 3회 나눠서 180g 주수 → 2:30 완료", "tips": "드립백도 블루밍하면 맛이 확 달라집니다", "description": "편의점 드립백도 맛있게 추출하는 팁"},
            {"title": "V60 원컵 레시피", "brew_method": "V60", "grind_size": "Medium-Fine", "water_temp": 92, "coffee_amount": 12, "water_amount": 200, "brew_time": 150, "ratio": "1:16.7", "steps": "01 사이즈 V60 → 12g 커피 → 25g 블루밍 → 2회 나눠서 총 200g → 2:30 완료", "tips": "소량 추출 시 분쇄도를 약간 가늘게", "description": "혼자 마시기 딱 좋은 1인분 V60 레시피"},
            {"title": "플랫화이트 스타일", "brew_method": "Espresso", "grind_size": "Fine", "water_temp": 93, "coffee_amount": 18, "water_amount": 36, "brew_time": 28, "ratio": "1:2", "steps": "더블샷 추출 → 마이크로폼 우유 120ml → 얇은 우유층으로 마무리", "tips": "우유 텍스쳐링이 핵심, 마이크로폼을 얇게", "description": "호주 스타일 플랫화이트 레시피"},
            {"title": "콜드 에스프레소 토닉", "brew_method": "Espresso", "grind_size": "Fine", "water_temp": 93, "coffee_amount": 18, "water_amount": 36, "brew_time": 28, "ratio": "에스프레소:토닉 1:4", "steps": "잔에 얼음 가득 → 토닉워터 150ml → 더블 에스프레소를 얼음 위에 천천히", "tips": "층이 분리되게 천천히 부으면 비주얼 업!", "description": "에스프레소 토닉, 여름 시그니처 음료"},
            {"title": "칼리타 웨이브", "brew_method": "Kalita Wave", "grind_size": "Medium", "water_temp": 91, "coffee_amount": 20, "water_amount": 300, "brew_time": 210, "ratio": "1:15", "steps": "필터 린싱 → 20g 커피 → 50g 블루밍 40초 → 5회 균등 푸어링 → 3:30 완료", "tips": "플랫 바텀이라 균일한 추출이 장점", "description": "안정적이고 재현성 높은 칼리타 웨이브 레시피"},
            {"title": "스팀펑크 브루잉", "brew_method": "Steampunk", "grind_size": "Medium", "water_temp": 94, "coffee_amount": 22, "water_amount": 350, "brew_time": 240, "ratio": "1:15.9", "steps": "자동 사이클 설정 → 수온 94도 → 침지 시간 3분 → 진공 추출 → 서빙", "tips": "머신이 대부분 자동이지만 분쇄도가 핵심 변수", "description": "하이테크 스팀펑크 브루어로 추출하는 미래형 커피"},
            {"title": "베트남 핀 드립", "brew_method": "Vietnamese Phin", "grind_size": "Coarse", "water_temp": 96, "coffee_amount": 25, "water_amount": 170, "brew_time": 300, "ratio": "1:6.8 + 연유", "steps": "핀 필터에 커피 → 프레스 → 소량 물로 블루밍 → 나머지 물 투입 → 5분 천천히 드립 → 연유와 섞기", "tips": "연유의 양으로 단맛을 조절하세요", "description": "달콤하고 진한 베트남 전통 핀 드립 커피"},
            {"title": "교토 슬로우 드립", "brew_method": "Cold Drip", "grind_size": "Medium-Coarse", "water_temp": 4, "coffee_amount": 40, "water_amount": 500, "brew_time": 480, "ratio": "1:12.5", "steps": "상부 물탱크에 얼음물 → 드립 속도 초당 1방울 조절 → 8시간 추출 → 12시간 숙성", "tips": "추출 속도가 맛을 결정하는 핵심 변수", "description": "8시간 한 방울씩, 극한의 교토 슬로우 드립"},
            {"title": "퍼콜레이터 캠핑 커피", "brew_method": "Percolator", "grind_size": "Coarse", "water_temp": 96, "coffee_amount": 40, "water_amount": 600, "brew_time": 420, "ratio": "1:15", "steps": "하부에 물 → 바스켓에 커피 → 중불 가열 → 보글보글 시작하면 약불 7분 → 완료", "tips": "캠핑장에서 최고의 커피 경험!", "description": "야외에서 즐기는 클래식 퍼콜레이터 레시피"},
            {"title": "이브릭 초콜릿 커피", "brew_method": "Turkish", "grind_size": "Extra Fine", "water_temp": 70, "coffee_amount": 12, "water_amount": 120, "brew_time": 240, "ratio": "1:10 + 코코아 5g", "steps": "이브릭에 커피+코코아+설탕+물 → 약불 가열 → 거품 3회 올리기 → 데미타세잔에 서빙", "tips": "고급 코코아 파우더를 사용하면 풍미 UP", "description": "초콜릿과 커피의 터키식 마리아주"},
            {"title": "에어로프레스 아이스", "brew_method": "Aeropress", "grind_size": "Fine", "water_temp": 96, "coffee_amount": 20, "water_amount": 100, "brew_time": 60, "ratio": "1:5 + 얼음 150g", "steps": "인버트 → 20g 커피 → 96도 물 100g → 스월 → 1분 후 얼음 위 플런지", "tips": "고농도 추출 후 급냉이 핵심", "description": "에어로프레스로 만드는 아이스 커피 레시피"},
            {"title": "핸드드립 브라질 내추럴", "brew_method": "V60", "grind_size": "Medium", "water_temp": 88, "coffee_amount": 20, "water_amount": 320, "brew_time": 210, "ratio": "1:16", "steps": "낮은 수온으로 시작 → 40g 블루밍 → 천천히 3회 주수 → 단맛 극대화", "tips": "내추럴 원두는 낮은 수온에서 단맛이 극대화", "description": "브라질 내추럴 원두에 최적화된 V60 레시피"},
            {"title": "하리오 스위치", "brew_method": "Hario Switch", "grind_size": "Medium-Fine", "water_temp": 93, "coffee_amount": 18, "water_amount": 280, "brew_time": 180, "ratio": "1:15.6", "steps": "스위치 닫기 → 필터 린싱 → 커피 투입 → 물 280g → 2분 침지 → 스위치 열어 드립", "tips": "침지 시간으로 바디감을 조절할 수 있어요", "description": "하리오 스위치의 침지+드립 하이브리드 레시피"},
            {"title": "에스프레소 아포가토", "brew_method": "Espresso", "grind_size": "Fine", "water_temp": 93, "coffee_amount": 18, "water_amount": 30, "brew_time": 25, "ratio": "에스프레소 30ml + 젤라토", "steps": "리스트레또 추출 30ml → 바닐라 젤라토/아이스크림 1스쿱 → 에스프레소 붓기", "tips": "추출 직후 바로 아이스크림 위에 부어야 온도 대비 극대화", "description": "에스프레소와 아이스크림의 완벽한 디저트 조합"},
            {"title": "오트밀크 라떼", "brew_method": "Espresso", "grind_size": "Fine", "water_temp": 93, "coffee_amount": 18, "water_amount": 36, "brew_time": 28, "ratio": "1:2 + 오트밀크 180ml", "steps": "더블샷 추출 → 바리스타용 오트밀크 스팀 → 마이크로폼 텍스쳐링 → 라떼아트", "tips": "바리스타 에디션 오트밀크가 거품이 잘 나요", "description": "비건 친화적인 오트밀크 라떼 레시피"},
            {"title": "에어로프레스 차가운 블룸", "brew_method": "Aeropress", "grind_size": "Medium", "water_temp": 60, "coffee_amount": 15, "water_amount": 220, "brew_time": 300, "ratio": "1:14.7", "steps": "인버트 → 60도 물 220g → 5분 긴 스티핑 → 천천히 플런지", "tips": "낮은 수온 + 긴 추출로 부드러운 맛", "description": "저온 장시간 추출의 독특한 에어로프레스 레시피"},
            {"title": "보틀넥 커피 리큐어", "brew_method": "Cold Brew", "grind_size": "Coarse", "water_temp": 4, "coffee_amount": 100, "water_amount": 500, "brew_time": 1440, "ratio": "1:5 원액 + 설탕시럽", "steps": "콜드브루 원액 추출 24시간 → 설탕시럽 100ml → 바닐라빈 1/4개 → 병에 담아 냉장 숙성 3일", "tips": "우유와 섞으면 커피 밀크리큐어!", "description": "집에서 만드는 커피 리큐어 (무알코올)"},
            {"title": "더블월 프렌치프레스", "brew_method": "French Press", "grind_size": "Coarse", "water_temp": 94, "coffee_amount": 35, "water_amount": 500, "brew_time": 300, "ratio": "1:14.3", "steps": "35g 커피 → 물 투입 → 2분 후 크러스트 스쿱 → 추가 3분 대기 → 매우 천천히 플런지", "tips": "크러스트를 걷어내면 프렌치프레스도 깔끔해집니다", "description": "제임스 호프만 스타일의 프렌치프레스 테크닉"},
            {"title": "캐스케이드 푸어오버", "brew_method": "V60", "grind_size": "Medium", "water_temp": 91, "coffee_amount": 15, "water_amount": 250, "brew_time": 180, "ratio": "1:16.7", "steps": "필터 린싱 → 15g → 30g 블루밍 → 25g씩 8회 계단식 주수 → 3:00 완료", "tips": "소량 다회 주수로 균일한 추출을 유도", "description": "계단식 주수로 추출 균일도를 높이는 테크닉"},
        ]

        recipes = []
        now = datetime.now(timezone.utc)
        for i, data in enumerate(recipe_templates):
            user = users[i % len(users)]
            bean = beans[i % len(beans)]
            recipe = Recipe(
                **data,
                bean_id=bean.id,
                owner_id=user.id,
                is_public=True,
                overall_rating=round(random.uniform(3.5, 5.0), 1),
                taste_rating=random.randint(3, 5),
                body_rating=random.randint(3, 5),
                acidity_rating=random.randint(2, 5),
                sweetness_rating=random.randint(3, 5),
                view_count=random.randint(50, 3000),
                likes_count=random.randint(5, 200),
                created_at=now - timedelta(days=random.randint(1, 120)),
            )
            self.db.add(recipe)
            recipes.append(recipe)
        self.db.commit()
        for r in recipes:
            self.db.refresh(r)
        logger.info(f"Created {len(recipes)} recipes")
        return recipes

    def _create_articles(self, users):
        article_data = [
            {"title": "2026 스페셜티 커피 트렌드 TOP 10", "summary": "올해 주목해야 할 스페셜티 커피 시장의 핵심 트렌드를 분석합니다.", "content": "2026년 스페셜티 커피 업계는 큰 변화를 맞이하고 있습니다.\n\n## 1. 발효 프로세싱의 진화\n아나에로빅(Anaerobic) 발효를 넘어, 특정 효모를 접종하는 이노큘레이션(Inoculation) 기법이 대세로 자리잡고 있습니다.\n\n## 2. AI 기반 로스팅\nCropster와 같은 로스팅 소프트웨어에 AI 프로파일링이 도입되어, 생두 특성에 맞는 최적 로스팅 커브를 자동으로 추천합니다.\n\n## 3. 카본 뉴트럴 커피\n탄소 발자국을 추적하고 상쇄하는 커피 공급망이 확대되고 있습니다.\n\n## 4. 마이크로 로트의 세분화\n단일 농장을 넘어 단일 나무, 단일 배치 단위의 극소량 로트가 인기를 끌고 있습니다.\n\n## 5. 대체 우유 전쟁\n오트밀크를 넘어 피스타치오, 헴프, 감자 우유까지 바리스타 에디션이 출시되고 있습니다."},
            {"title": "홈카페 그라인더 선택 가이드 2026", "summary": "입문자부터 마니아까지, 예산별 추천 그라인더를 소개합니다.", "content": "홈카페의 핵심은 그라인더입니다. 2026년 기준 최고의 선택을 안내합니다.\n\n## 입문용 (10만원 이하)\n- Timemore C2 MAX: 가성비의 끝판왕, 균일한 분쇄\n- 1Zpresso Q2: 휴대성과 성능의 밸런스\n\n## 중급 (10-30만원)\n- Timemore Sculptor 064: 전동의 편리함과 핸드밀의 품질\n- Fellow Ode Gen 2: 깔끔한 디자인, SSP 버 호환\n\n## 고급 (30만원 이상)\n- DF64 Gen 2: 제로 리텐션, 싱글도징\n- Niche Zero: 올라운더, 에스프레소부터 드립까지\n- Weber EG-1: 최상급 균일도, 그라인더의 끝"},
            {"title": "에티오피아 vs 케냐 원두 비교 분석", "summary": "아프리카 양대 산지의 맛 프로필을 상세 비교합니다.", "content": "에티오피아와 케냐는 모두 아프리카 커피의 양대 산맥이지만, 그 맛은 확연히 다릅니다.\n\n## 에티오피아\n- 품종: 헤어룸 (다양한 야생 품종)\n- 특징: 꽃향, 베르가못, 홍차, 블루베리\n- 프로세싱: 워시드(깔끔) / 내추럴(과일향 폭발)\n- 대표 산지: 예가체프, 시다모, 구지\n\n## 케냐\n- 품종: SL28, SL34 (연구소 개발 품종)\n- 특징: 블랙커런트, 자몽, 토마토, 강한 산미\n- 프로세싱: 주로 더블 워시드 (72시간 발효)\n- 대표 산지: 니에리, 키암부, 에부루\n\n## 추출 추천\n에티오피아: V60, 가벼운 추출로 향 극대화\n케냐: 에어로프레스, 강한 산미를 바디감과 밸런스"},
            {"title": "프렌치프레스 완벽 가이드", "summary": "프렌치프레스를 제대로 사용하는 방법, A to Z.", "content": "프렌치프레스는 가장 쉬우면서도 가장 과소평가된 추출 도구입니다.\n\n## 왜 프렌치프레스인가?\n풀 이머전(완전 침지) 방식으로 오일과 바디를 최대한 추출합니다.\n\n## 핵심 변수\n1. 분쇄도: 굵게! 소금 알갱이 정도\n2. 물 온도: 94-96°C\n3. 침지 시간: 4분 (제임스 호프만 기준)\n4. 크러스트 처리: 4분 후 크러스트를 스푼으로 걷어내기\n\n## 프로 팁\n- 플런지를 끝까지 누르지 마세요, 필터 바로 위까지만\n- 바로 따르세요, 프레스에 두면 과추출\n- 프리히트 필수!"},
            {"title": "워터 브루잉: 물이 커피 맛을 바꾼다", "summary": "추출수의 TDS와 미네랄 함량이 커피 맛에 미치는 영향.", "content": "같은 원두, 같은 레시피라도 물이 다르면 맛이 완전히 달라집니다.\n\n## TDS (총 용존 고형물)\n- SCA 기준: 75-250 ppm (이상적: 150 ppm)\n- 너무 낮으면: 밋밋하고 평평한 맛\n- 너무 높으면: 탁하고 무거운 맛\n\n## 핵심 미네랄\n- 칼슘: 바디감과 단맛 강화\n- 마그네슘: 산미와 과일향 추출 촉진\n- 중탄산염: 산미를 완충 (적당량 필요)\n\n## 추천 물\n1. Third Wave Water (미네랄 패킷)\n2. 브리타 필터 + 증류수 블렌딩\n3. 삼다수 (한국 기준 무난한 선택)"},
            {"title": "라떼아트 입문: 하트부터 로제타까지", "summary": "라떼아트 기초부터 고급 패턴까지 단계별 가이드.", "content": "라떼아트는 연습과 이해의 예술입니다.\n\n## 기본 원리\n1. 올바른 밀크 스티밍 (마이크로폼 생성)\n2. 적절한 에스프레소 크레마\n3. 피칭 높이와 속도 조절\n\n## 단계별 패턴\n\n### 1단계: 하트\n- 컵 기울이기 → 높은 위치에서 우유 붓기 → 컵의 1/3 → 낮추어 중심에 → 직선으로 관통\n\n### 2단계: 로제타\n- 하트 기본 → 좌우로 흔들며 붓기 → 잎사귀 패턴 → 직선 관통\n\n### 3단계: 튤립\n- 푸시-정지 반복 → 3-5개 층 쌓기 → 마지막 관통\n\n## 연습 팁\n- 하루 20잔 이상 연습 추천\n- 처음엔 물+세제로 연습 (비용 절약)"},
            {"title": "커핑(Cupping) 프로토콜 가이드", "summary": "SCA 기준 커핑 절차와 평가 방법을 상세히 설명합니다.", "content": "커핑은 커피를 객관적으로 평가하는 표준 방법입니다.\n\n## SCA 커핑 프로토콜\n1. 커피 8.25g / 물 150ml (비율 1:18.18)\n2. 분쇄: 미디엄-코스 (큐그라인더 기준 #4)\n3. 수온: 93°C\n4. 주수 후 4분 대기\n5. 크러스트 브레이킹 (3회 스쿱)\n6. 스컴 제거\n7. 8-10분 후 테이스팅 시작\n\n## 평가 항목 (각 10점)\n- Fragrance/Aroma (향)\n- Flavor (맛)\n- Aftertaste (후미)\n- Acidity (산미)\n- Body (바디)\n- Balance (밸런스)\n- Sweetness (단맛)\n- Uniformity (균일성)\n- Clean Cup (깔끔함)\n- Overall (종합)"},
            {"title": "에스프레소 머신 없이 에스프레소 만들기", "summary": "에스프레소 머신이 없어도 진한 커피를 추출하는 5가지 방법.", "content": "비싼 에스프레소 머신 없이도 에스프레소 농도의 커피를 즐길 수 있습니다.\n\n## 1. 에어로프레스\n- 미세 분쇄 18g + 55ml 물\n- 강한 프레스 → 에스프레소 농도\n\n## 2. 모카포트\n- 가장 전통적인 대안\n- 9bar는 아니지만 진한 추출 가능\n\n## 3. 넌투라 핸드 에스프레소\n- Flair, Cafelat Robot 등 수동 레버 머신\n- 실제 9bar 압력 구현 가능\n\n## 4. Wacaco Nanopresso\n- 휴대용 에스프레소 메이커\n- 최대 18bar 압력\n\n## 5. 터키식 커피\n- 에스프레소보다 진한 농도\n- 오리지널 '강한 커피'"},
            {"title": "커피와 건강: 2026 최신 연구 결과", "summary": "하루 몇 잔이 적당한가? 최신 의학 연구를 정리합니다.", "content": "커피와 건강에 대한 2026년 최신 연구 결과를 정리했습니다.\n\n## 긍정적 효과\n- 하루 3-5잔: 심혈관 질환 위험 15% 감소 (NEJM 2025)\n- 간암 위험 40% 감소 (WHO 분석)\n- 제2형 당뇨 위험 25% 감소\n- 파킨슨병 위험 감소\n- 인지 기능 향상 (집중력, 기억력)\n\n## 주의 사항\n- 카페인 민감도는 유전자(CYP1A2)에 따라 다름\n- 임신 중: 하루 200mg 이하 권장\n- 불안장애: 카페인 제한 필요\n- 수면: 취침 6시간 전 이후 카페인 금지\n\n## 결론\n건강한 성인 기준, 하루 3-4잔의 블랙커피는 건강에 유익합니다."},
            {"title": "싱글 오리진 vs 블렌드: 무엇을 선택할까?", "summary": "싱글 오리진과 블렌드의 차이, 장단점, 선택 가이드.", "content": "싱글 오리진과 블렌드, 어떤 것이 더 좋을까요?\n\n## 싱글 오리진\n- 단일 산지/농장의 원두\n- 테루아(terroir)의 고유한 맛\n- 드립, 핸드드립에 적합\n- 계절성 (크롭 사이클)\n\n## 블렌드\n- 2개 이상 산지 원두 혼합\n- 일관된 맛 프로필\n- 에스프레소에 최적화 가능\n- 연중 안정적 공급\n\n## 선택 기준\n- 산미와 개성을 원한다면 → 싱글 오리진\n- 밸런스와 일관성을 원한다면 → 블렌드\n- 라떼용 → 블렌드 (우유와 밸런스)\n- 블랙 커피 → 싱글 오리진 (개성 탐험)"},
            {"title": "커피 보관의 과학", "summary": "원두 신선도를 최대한 유지하는 보관 방법.", "content": "로스팅 후 커피의 맛은 시간이 지남에 따라 변합니다.\n\n## 커피의 4대 적\n1. 산소: 산화로 인한 맛 변질\n2. 습기: 수분 흡수로 곰팡이 위험\n3. 빛: UV가 화학적 변화 촉진\n4. 열: 가속화된 노화\n\n## 최적 보관 방법\n- 불투명 밀폐 용기 (원웨이 밸브 추천)\n- 서늘하고 어두운 곳 (15-25°C)\n- 원두 상태로 보관 (분쇄하지 말 것)\n- 소분 보관 (공기 접촉 최소화)\n\n## 기간별 가이드\n- 에스프레소: 로스팅 후 7-21일 최적\n- 필터 커피: 로스팅 후 4-14일 최적\n- 콜드브루: 로스팅 후 2-4주도 OK\n- 냉동 보관: 최대 3개월 (원두 상태)"},
            {"title": "V60 마스터 클래스: 프로 바리스타의 비밀", "summary": "대회 입상 바리스타들의 V60 추출 노하우를 공개합니다.", "content": "V60은 간단해 보이지만 마스터하기 가장 어려운 도구입니다.\n\n## 프로의 5가지 비밀\n\n### 1. RDT (Ross Droplet Technique)\n분쇄 전 원두에 물 한 방울 → 정전기 제거 → 균일한 분쇄\n\n### 2. WDT (Weiss Distribution Technique)\n분쇄 후 바늘로 젓기 → 클럼프 제거 → 균일한 추출\n\n### 3. 블루밍 시간 조절\n- 라이트 로스트: 45초 (CO2가 많음)\n- 미디엄: 30초\n- 다크: 20초 (가스가 적음)\n\n### 4. 물줄기 높이\n- 높은 위치: 교반 강함, 추출 촉진\n- 낮은 위치: 부드러운 추출, 바디 강화\n\n### 5. 온도 서핑\n블루밍은 높은 온도, 본 추출은 1-2도 낮추기"},
            {"title": "세계 커피 산지 투어: 가봐야 할 10곳", "summary": "커피 애호가라면 꼭 방문해야 할 산지 10선.", "content": "커피를 사랑한다면 산지를 직접 방문해보세요.\n\n## 1. 에티오피아 예가체프\n커피의 고향, 야생 커피 숲 트래킹\n\n## 2. 콜롬비아 살렌토\n커피 삼각지대의 심장, 핀카 투어\n\n## 3. 코스타리카 타라주\n지속가능한 커피 농장 체험\n\n## 4. 파나마 보케테\n게이샤 품종의 성지\n\n## 5. 과테말라 안티구아\n화산 토양과 커피의 만남\n\n## 6. 케냐 니에리\nSL28 품종의 고향\n\n## 7. 인도네시아 토라자\n습식 탈곡의 현장\n\n## 8. 예멘 하라즈\n전통 테라스 농법\n\n## 9. 자메이카 블루마운틴\n세계에서 가장 비싼 커피 산지\n\n## 10. 하와이 코나\n미국 유일의 커피 산지"},
            {"title": "에어로프레스 대회 레시피 분석 (2024-2025)", "summary": "최근 2년간 에어로프레스 챔피언십 우승 레시피를 분석합니다.", "content": "에어로프레스 챔피언십은 매년 혁신적인 레시피가 등장합니다.\n\n## 2025 월드 챔피언\n- 커피: 16g (내추럴 에티오피아)\n- 물: 230g, 80°C\n- 분쇄: 미디엄-파인\n- 인버트 방식\n- 스티핑: 2분 30초\n- 특이점: 저온 추출\n\n## 2024 월드 챔피언\n- 커피: 18g (워시드 콜롬비아)\n- 물: 200g, 85°C\n- 바이패스: 100ml 상온 물\n- 스티핑: 1분 30초\n\n## 트렌드 분석\n1. 수온 하향 추세 (85°C → 80°C)\n2. 바이패스 기법 증가\n3. 긴 스티핑 시간\n4. 내추럴 프로세스 원두 선호"},
            {"title": "카페 창업 체크리스트 2026", "summary": "카페 오픈 전 반드시 확인해야 할 핵심 항목들.", "content": "카페 창업을 준비하고 계신가요? 2026년 기준 체크리스트입니다.\n\n## 1. 상권 분석\n- 유동인구 (평일/주말 구분)\n- 경쟁 카페 반경 500m 조사\n- 주차 가능 여부\n- 월세 대비 예상 매출\n\n## 2. 장비 선정\n- 에스프레소 머신: 린베이 2그룹 이상\n- 그라인더: 피크 타임 대응 가능한 온디맨드\n- 정수: 역삼투압(RO) + 미네랄 조정\n- POS: 태블릿 기반 클라우드 POS\n\n## 3. 메뉴 구성\n- 에스프레소 베이스 5-8종\n- 논커피 3-5종\n- 디저트/베이커리 3-5종\n- 시즌 메뉴 2-3종\n\n## 4. 마케팅\n- 인스타그램 피드 통일감\n- 네이버 플레이스 등록\n- 오픈 이벤트 기획"},
            {"title": "디카페인 커피의 진실", "summary": "디카페인은 정말 카페인이 없을까? 디카페인 처리 방법과 맛의 차이.", "content": "디카페인 커피에 대한 오해와 진실을 파헤칩니다.\n\n## 디카페인 처리 방법\n\n### 1. Swiss Water Process\n- 화학물질 불사용\n- 물과 탄소 필터 사용\n- 카페인 99.9% 제거\n- 맛 손실 최소\n\n### 2. CO2 Process\n- 초임계 CO2 사용\n- 카페인만 선택적 제거\n- 고비용이지만 최고 품질\n\n### 3. MC (Methylene Chloride) Process\n- 가장 저렴한 방법\n- 화학 용매 사용\n- FDA 승인 (잔류량 10ppm 이하)\n\n## 카페인 잔류량\n- 디카페인에도 2-15mg 카페인 존재\n- 일반 커피: 80-120mg\n- 카페인 민감자는 주의 필요\n\n## 맛의 차이\n- 현대 스페셜티 디카페인은 거의 차이 없음\n- Swiss Water + 좋은 생두 = 충분히 맛있음"},
            {"title": "홈로스팅 입문 가이드", "summary": "집에서 커피를 로스팅하는 방법, 장비, 팁을 소개합니다.", "content": "홈로스팅은 커피 취미의 궁극입니다.\n\n## 입문 장비\n1. 수망 로스터 (1만원): 프라이팬 로스팅\n2. 팝콘 메이커 (5만원): 의외로 균일한 로스팅\n3. 비해브 로스터 (30만원): 입문용 전동\n4. 알리 커피 로스터 (50만원): 반자동\n\n## 로스팅 기본\n- 1차 크랙 (약 200°C): 라이트-미디엄\n- 2차 크랙 (약 225°C): 미디엄다크-다크\n\n## 프로파일 기본\n1. 건조 단계 (0-8분): 수분 제거\n2. 마이야르 반응 (8-10분): 갈변 시작\n3. 발전 단계 (1차 크랙 후): 맛 발현\n\n## 초보 팁\n- 1차 크랙 후 1-2분에서 배출 (미디엄)\n- 환기 필수! 연기가 많이 남\n- 로스팅 후 12-24시간 디개싱"},
            {"title": "커피 용어 사전: 알아두면 좋은 50가지", "summary": "커피 초보자를 위한 필수 용어 모음.", "content": "커피 세계의 필수 용어를 정리했습니다.\n\n## 추출 관련\n- **블루밍(Blooming)**: 뜸들이기, CO2 방출\n- **바이패스(Bypass)**: 추출 후 물 추가\n- **채널링(Channeling)**: 물이 한쪽으로 치우치는 현상\n- **TDS**: Total Dissolved Solids, 추출 농도\n- **추출 수율**: 녹아든 커피 성분 비율 (18-22% 이상적)\n\n## 원두 관련\n- **SCA 스코어**: 80점 이상이 스페셜티\n- **QC/QA 그레이더**: 커피 등급 평가사\n- **크롭(Crop)**: 수확 연도\n- **그린빈**: 생두 (볶기 전 상태)\n\n## 로스팅 관련\n- **ROR(Rate of Rise)**: 온도 상승률\n- **디벨롭먼트**: 1차 크랙 후 발전 시간\n- **디개싱**: 로스팅 후 CO2 방출 기간\n\n## 프로세싱\n- **워시드(Washed)**: 수세 처리\n- **내추럴(Natural)**: 건식 처리\n- **허니(Honey)**: 반건식 처리\n- **아나에로빅(Anaerobic)**: 무산소 발효"},
            {"title": "최고의 커피 유튜브 채널 추천 2026", "summary": "커피 지식을 쌓을 수 있는 국내외 유튜브 채널 추천.", "content": "영상으로 커피를 배우고 싶다면!\n\n## 해외 채널\n1. **James Hoffmann**: 커피 유튜브의 GOAT, 깊이 있는 리뷰\n2. **Lance Hedrick**: 시각적으로 아름다운 추출 영상\n3. **Sprometheus**: 에스프레소 전문, 데이터 기반\n4. **European Coffee Trip**: 유럽 카페 투어\n5. **Morgan Drinks Coffee**: 장비 리뷰 전문\n\n## 국내 채널\n1. **커피TV**: 국내 최대 커피 미디어\n2. **신영식의 오모택스**: 부산 커피 문화\n3. **안스커피**: 홈카페 장비 리뷰\n4. **커피 블레이크**: 트렌디한 카페 투어"},
            {"title": "물 온도에 따른 추출 변화 실험", "summary": "80°C부터 100°C까지, 5°C 단위로 추출 결과를 비교합니다.", "content": "동일한 원두, 동일한 레시피에서 물 온도만 바꿔 실험했습니다.\n\n## 실험 조건\n- 원두: 에티오피아 예가체프 (라이트 로스트)\n- 도구: V60\n- 분량: 18g / 300ml\n\n## 결과\n\n### 80°C\n산미: ★☆☆☆☆ | 바디: ★★☆☆☆ | 단맛: ★★★☆☆\n→ 약한 추출, 밋밋하고 시큼한 맛\n\n### 85°C\n산미: ★★★☆☆ | 바디: ★★★☆☆ | 단맛: ★★★★☆\n→ 부드러운 산미, 단맛 부각\n\n### 90°C\n산미: ★★★★☆ | 바디: ★★★★☆ | 단맛: ★★★★★\n→ 밸런스 최고점, 추천 온도\n\n### 93°C (SCA 기준)\n산미: ★★★★★ | 바디: ★★★★☆ | 단맛: ★★★★☆\n→ 밝은 산미가 돋보이는 클래식한 맛\n\n### 96°C\n산미: ★★★★☆ | 바디: ★★★★★ | 단맛: ★★★☆☆\n→ 바디 강화, 약간의 쓴맛 등장\n\n### 100°C\n산미: ★★★☆☆ | 바디: ★★★★★ | 단맛: ★★☆☆☆\n→ 과추출 시작, 떫은맛"},
            {"title": "2026 서울 스페셜티 카페 TOP 20", "summary": "서울에서 꼭 가봐야 할 스페셜티 커피숍 리스트.", "content": "2026년 서울 최고의 스페셜티 카페를 소개합니다.\n\n## 강남/서초\n1. Fritz Coffee: 한남동 본점, 시즌 블렌드 필수\n2. Center Coffee: 신사동, 게이샤 전문\n3. Felt Coffee: 압구정, 미니멀 공간\n\n## 성수/건대\n4. Mano Coffee: 성수동 대표 카페\n5. Anthracite: 구두 공장 개조 카페\n6. Mesh Coffee: 건대입구, 라이트 로스트\n\n## 종로/을지\n7. Namusairo: 종로, 자체 로스팅\n8. Coffee Libre: 서촌, 스페셜티 선구자\n9. Hell Cafe: 을지로, 산업 디자인 카페\n\n## 이태원/한남\n10. Cafe Knotted: 커피+도넛 시너지\n\n각 카페의 시그니처 메뉴와 추천 원두는 앱에서 확인하세요."},
            {"title": "커피 추출 실패 분석: 맛이 이상할 때 체크리스트", "summary": "쓴맛, 신맛, 밍밍한 맛... 원인과 해결법을 정리합니다.", "content": "커피가 맛없을 때, 어디가 문제인지 찾는 방법입니다.\n\n## 너무 쓴 경우\n원인:\n- 과추출 (시간이 너무 길거나 물이 너무 뜨거움)\n- 분쇄가 너무 가늘음\n해결: 분쇄도 굵게, 수온 낮추기, 추출 시간 단축\n\n## 너무 신 경우\n원인:\n- 과소추출 (시간이 짧거나 물이 미지근함)\n- 분쇄가 너무 굵음\n해결: 분쇄도 가늘게, 수온 올리기, 추출 시간 늘리기\n\n## 밍밍한 경우\n원인:\n- 커피 양 부족\n- 물 양 과다\n- 원두 신선도 문제\n해결: 비율 확인 (1:15-17), 원두 교체\n\n## 텁텁한 경우\n원인:\n- 미분 과다\n- 필터 품질 문제\n해결: RDT 적용, 미분 체거름, 필터 교체"},
            {"title": "에스프레소 다이얼인 완벽 가이드", "summary": "에스프레소 머신의 추출 변수를 조절하는 체계적인 방법.", "content": "에스프레소 다이얼인은 과학적으로 접근해야 합니다.\n\n## 기본 파라미터\n- 도징량: 18-20g (더블샷 기준)\n- 추출량: 36-40ml (1:2 비율)\n- 추출 시간: 25-30초\n- 추출 온도: 90-96°C\n- 압력: 9bar\n\n## 다이얼인 순서\n1. 분쇄도 설정 → 25-30초에 맞추기\n2. 맛 평가 → 쓰면 굵게, 시면 가늘게\n3. 온도 조절 → 1-2°C 단위로\n4. 비율 조절 → 1:1.5 ~ 1:2.5\n\n## 프로 팁\n- 한 번에 하나의 변수만 변경\n- 3샷 연속 같은 조건으로 확인\n- 로스팅 후 날짜에 따라 재조정 필요"},
            {"title": "지속가능한 커피: 공정무역 그 너머", "summary": "공정무역, 직접 무역, 환경 인증의 차이와 의미.", "content": "커피 한 잔의 윤리적 선택에 대해 생각해봅니다.\n\n## 공정무역 (Fair Trade)\n- 최저 가격 보장 ($1.40/lb)\n- 인증 비용이 농부에게 부담\n- 품질보다 가격에 초점\n\n## 직접 무역 (Direct Trade)\n- 로스터가 농부와 직접 거래\n- 공정무역보다 높은 가격 가능\n- 품질 인센티브 존재\n- 하지만 검증 시스템 부재\n\n## 환경 인증\n- Rainforest Alliance: 생태계 보호\n- Bird Friendly: 그늘 재배\n- Organic: 유기농 인증\n\n## 소비자가 할 수 있는 것\n1. 투명한 소싱 정보를 공개하는 로스터 선택\n2. 시즌 원두 구매 (신선한 크롭)\n3. 스페셜티 등급 구매 (농부에게 높은 가격)"},
            {"title": "커피와 음식 페어링 가이드", "summary": "커피와 어울리는 음식 조합, 맛의 시너지를 탐구합니다.", "content": "와인처럼 커피에도 페어링이 있습니다.\n\n## 라이트 로스트\n- 에티오피아 워시드 + 레몬 타르트\n- 케냐 + 베리류 디저트\n- 파나마 게이샤 + 백도 셔벗\n\n## 미디엄 로스트\n- 콜롬비아 + 초콜릿 크루아상\n- 과테말라 + 호두 브라우니\n- 코스타리카 허니 + 치즈케이크\n\n## 다크 로스트\n- 인도네시아 만델링 + 다크 초콜릿\n- 브라질 내추럴 + 티라미수\n- 에스프레소 + 카놀리\n\n## 의외의 조합\n- 콜드브루 + 치즈 (고다, 브리)\n- 에스프레소 + 올리브오일 (트렌드!)\n- V60 에티오피아 + 회(참치, 연어)"},
        ]

        article_thumbs = [
            "https://images.unsplash.com/photo-1442512595331-e89e73853f31?w=600",
            "https://images.unsplash.com/photo-1587734195503-904fca47e0e9?w=600",
            "https://images.unsplash.com/photo-1559525839-b184a4d698c7?w=600",
            "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=600",
            "https://images.unsplash.com/photo-1518057111178-44a106bad636?w=600",
            "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=600",
            "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=600",
            "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=600",
            "https://images.unsplash.com/photo-1497935586351-b67a49e012bf?w=600",
            "https://images.unsplash.com/photo-1510707577719-ae7c14805e3a?w=600",
            "https://images.unsplash.com/photo-1485808191679-5f86510681a2?w=600",
            "https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=600",
            "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=600",
            "https://images.unsplash.com/photo-1504630083234-14187a9df0f5?w=600",
            "https://images.unsplash.com/photo-1511920170033-f8396924c348?w=600",
            "https://images.unsplash.com/photo-1498804103079-a6351b050096?w=600",
            "https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=600",
            "https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=600",
            "https://images.unsplash.com/photo-1611564494260-6f21b80af7ea?w=600",
            "https://images.unsplash.com/photo-1517701550927-30cf4ba1dba5?w=600",
            "https://images.unsplash.com/photo-1521302080334-4bebac2763a6?w=600",
            "https://images.unsplash.com/photo-1504753793650-d4a2b783c15e?w=600",
            "https://images.unsplash.com/photo-1445116572660-236099ec97a0?w=600",
            "https://images.unsplash.com/photo-1460518451285-97b6aa326961?w=600",
            "https://images.unsplash.com/photo-1507133750040-4a8f57021571?w=600",
        ]

        articles = []
        now = datetime.now(timezone.utc)
        for i, data in enumerate(article_data):
            user = users[i % len(users)]
            article = Article(
                **data,
                author_id=user.id,
                thumbnail_url=article_thumbs[i % len(article_thumbs)],
                is_published=True,
                view_count=random.randint(100, 5000),
                likes_count=random.randint(10, 300),
                created_at=now - timedelta(days=random.randint(1, 60)),
                published_at=now - timedelta(days=random.randint(1, 60)),
            )
            self.db.add(article)
            articles.append(article)
        self.db.commit()
        for a in articles:
            self.db.refresh(a)
        logger.info(f"Created {len(articles)} articles")
        return articles

    def _create_gears(self):
        gear_catalog = [
            {"name": "Comandante C40 MK4", "brand": "Comandante", "model": "C40 MK4", "gear_type": GearType.GRINDER, "description": "독일제 핸드 그라인더의 정점. 니트로 블레이드 버로 균일한 분쇄를 자랑합니다.", "image_url": "https://images.unsplash.com/photo-1587734195503-904fca47e0e9?w=400", "price_min": 320000, "price_max": 380000, "currency": "KRW", "is_recommended": True, "recommendation_reason": "핸드 그라인더 최고의 분쇄 균일도"},
            {"name": "Timemore C2 MAX", "brand": "Timemore", "model": "C2 MAX", "gear_type": GearType.GRINDER, "description": "10만원 이하 가성비 핸드 그라인더의 대표주자. 30g 용량으로 2인분까지 커버.", "image_url": "https://images.unsplash.com/photo-1517701550927-30cf4ba1dba5?w=400", "price_min": 55000, "price_max": 75000, "currency": "KRW", "is_recommended": True, "recommendation_reason": "입문자 최고 가성비"},
            {"name": "Fellow Ode Gen 2", "brand": "Fellow", "model": "Ode Gen 2", "gear_type": GearType.GRINDER, "description": "미니멀 디자인의 전동 그라인더. SSP 버 호환으로 업그레이드 가능.", "image_url": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400", "price_min": 350000, "price_max": 400000, "currency": "KRW", "is_recommended": True, "recommendation_reason": "전동 그라인더 입문 추천"},
            {"name": "DF64 Gen 2", "brand": "Turin", "model": "DF64 Gen 2", "gear_type": GearType.GRINDER, "description": "64mm 플랫버 싱글도징 그라인더. 제로 리텐션에 가까운 성능.", "image_url": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=400", "price_min": 400000, "price_max": 500000, "currency": "KRW", "is_recommended": False},
            {"name": "1Zpresso J-Max", "brand": "1Zpresso", "model": "J-Max", "gear_type": GearType.GRINDER, "description": "48mm 스테인리스 버. 에스프레소부터 드립까지 올라운드.", "image_url": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=400", "price_min": 200000, "price_max": 250000, "currency": "KRW", "is_recommended": True, "recommendation_reason": "에스프레소 가능한 핸드밀"},
            {"name": "Hario V60 드리퍼 02", "brand": "Hario", "model": "V60-02", "gear_type": GearType.BREWER, "description": "가장 널리 사용되는 푸어오버 드리퍼. 나선형 리브로 빠른 추출.", "image_url": "https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=400", "price_min": 8000, "price_max": 15000, "currency": "KRW", "is_recommended": True, "recommendation_reason": "드립 입문의 정석"},
            {"name": "Kalita Wave 185", "brand": "Kalita", "model": "Wave 185", "gear_type": GearType.BREWER, "description": "플랫 바텀 드리퍼. V60보다 균일하고 안정적인 추출.", "image_url": "https://images.unsplash.com/photo-1442512595331-e89e73853f31?w=400", "price_min": 25000, "price_max": 35000, "currency": "KRW", "is_recommended": True, "recommendation_reason": "일관된 추출이 장점"},
            {"name": "AeroPress Original", "brand": "AeroPress", "model": "Original", "gear_type": GearType.BREWER, "description": "세계에서 가장 다재다능한 브루어. 에스프레소부터 콜드브루까지.", "image_url": "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=400", "price_min": 40000, "price_max": 55000, "currency": "KRW", "is_recommended": True, "recommendation_reason": "만능 브루어, 여행용으로도 최고"},
            {"name": "Chemex Classic 6컵", "brand": "Chemex", "model": "Classic 6-Cup", "gear_type": GearType.BREWER, "description": "아이코닉한 디자인의 푸어오버 카라페. 두꺼운 필터로 깔끔한 맛.", "image_url": "https://images.unsplash.com/photo-1559525839-b184a4d698c7?w=400", "price_min": 60000, "price_max": 80000, "currency": "KRW", "is_recommended": False},
            {"name": "Clever Dripper", "brand": "Clever", "model": "Large", "gear_type": GearType.BREWER, "description": "침지+드립의 하이브리드. 초보자도 실패 없는 추출.", "image_url": "https://images.unsplash.com/photo-1497935586351-b67a49e012bf?w=400", "price_min": 25000, "price_max": 35000, "currency": "KRW", "is_recommended": True, "recommendation_reason": "초보자에게 가장 추천"},
            {"name": "Breville Bambino Plus", "brand": "Breville", "model": "Bambino Plus", "gear_type": GearType.ESPRESSO_MACHINE, "description": "컴팩트한 홈 에스프레소 머신. 자동 스팀, 3초 히팅.", "image_url": "https://images.unsplash.com/photo-1510707577719-ae7c14805e3a?w=400", "price_min": 450000, "price_max": 550000, "currency": "KRW", "is_recommended": True, "recommendation_reason": "홈 에스프레소 입문 추천"},
            {"name": "Flair Signature Pro 2", "brand": "Flair", "model": "Signature Pro 2", "gear_type": GearType.ESPRESSO_MACHINE, "description": "레버 수동 에스프레소 메이커. 전기 없이 진정한 에스프레소.", "image_url": "https://images.unsplash.com/photo-1485808191679-5f86510681a2?w=400", "price_min": 350000, "price_max": 450000, "currency": "KRW", "is_recommended": True, "recommendation_reason": "전기 없이 진짜 에스프레소"},
            {"name": "Fellow Stagg EKG", "brand": "Fellow", "model": "Stagg EKG", "gear_type": GearType.KETTLE, "description": "정밀 온도 조절 구스넥 전기 케틀. 0.1도 단위 설정.", "image_url": "https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=400", "price_min": 180000, "price_max": 220000, "currency": "KRW", "is_recommended": True, "recommendation_reason": "푸어오버 필수 장비"},
            {"name": "Hario Buono", "brand": "Hario", "model": "V60 Buono", "gear_type": GearType.KETTLE, "description": "클래식 구스넥 드립 포트. 가성비 좋은 기본형 케틀.", "image_url": "https://images.unsplash.com/photo-1518057111178-44a106bad636?w=400", "price_min": 35000, "price_max": 50000, "currency": "KRW", "is_recommended": False},
            {"name": "Timemore Black Mirror Plus", "brand": "Timemore", "model": "Black Mirror Plus", "gear_type": GearType.SCALE, "description": "0.1g 정밀도, 플로우레이트 측정, 블루투스 연동.", "image_url": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=400", "price_min": 70000, "price_max": 90000, "currency": "KRW", "is_recommended": True, "recommendation_reason": "가성비 커피 스케일 1위"},
            {"name": "Acaia Pearl S", "brand": "Acaia", "model": "Pearl S", "gear_type": GearType.SCALE, "description": "프로급 커피 스케일. 앱 연동, 추출 데이터 기록.", "image_url": "https://images.unsplash.com/photo-1498804103079-a6351b050096?w=400", "price_min": 200000, "price_max": 250000, "currency": "KRW", "is_recommended": False},
            {"name": "Hario V60 필터 02", "brand": "Hario", "model": "VCF-02-100W", "gear_type": GearType.FILTER, "description": "V60 전용 화이트 페이퍼 필터 100매.", "image_url": "https://images.unsplash.com/photo-1611564494260-6f21b80af7ea?w=400", "price_min": 6000, "price_max": 8000, "currency": "KRW", "is_recommended": True, "recommendation_reason": "V60 사용자 필수"},
            {"name": "Fellow Atmos 캐니스터", "brand": "Fellow", "model": "Atmos 1.2L", "gear_type": GearType.ACCESSORIES, "description": "진공 밀폐 원두 보관 캐니스터. 원두 신선도 최대 50% 연장.", "image_url": "https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=400", "price_min": 40000, "price_max": 55000, "currency": "KRW", "is_recommended": True, "recommendation_reason": "원두 보관의 정석"},
            {"name": "WDT 니들 툴", "brand": "Generic", "model": "WDT Tool", "gear_type": GearType.ACCESSORIES, "description": "에스프레소 퍽 분배용 니들 도구. 채널링 방지 필수 아이템.", "image_url": "https://images.unsplash.com/photo-1504630083234-14187a9df0f5?w=400", "price_min": 15000, "price_max": 30000, "currency": "KRW", "is_recommended": True, "recommendation_reason": "에스프레소 추출 품질 향상"},
            {"name": "커핑 스푼 세트", "brand": "Brewista", "model": "Cupping Spoon Set", "gear_type": GearType.ACCESSORIES, "description": "SCA 기준 커핑 스푼 6개 세트. 스테인리스 소재.", "image_url": "https://images.unsplash.com/photo-1511920170033-f8396924c348?w=400", "price_min": 25000, "price_max": 35000, "currency": "KRW", "is_recommended": False},
        ]

        gears = []
        for data in gear_catalog:
            gear = Gear(**data)
            self.db.add(gear)
            gears.append(gear)
        self.db.commit()
        for g in gears:
            self.db.refresh(g)
        logger.info(f"Created {len(gears)} gears")
        return gears

    def _create_gear_reviews(self, users, gears):
        review_templates = [
            ("최고의 선택이었습니다", "매일 사용하고 있는데 정말 만족스럽습니다. 품질이 뛰어나고 디자인도 예쁩니다.", "품질 우수, 디자인 좋음", "가격이 조금 높음"),
            ("가성비 최고", "이 가격에 이 성능이면 정말 훌륭합니다. 입문자에게 강력 추천!", "가격 대비 성능 좋음", "고급 기능은 부족"),
            ("2년째 사용 중", "오랜 기간 사용해도 성능 저하가 없습니다. 내구성이 뛰어나요.", "내구성 좋음, 안정적", "무게가 있음"),
            ("기대 이상입니다", "리뷰 보고 구매했는데 기대 이상이에요. 커피 맛이 확실히 달라졌습니다.", "맛 향상 체감됨", "사용법 학습 필요"),
            ("선물로 받았는데 대만족", "커피 좋아하는 친구에게 받았는데 인생템이 되었습니다.", "사용 편의성 좋음", "특별한 단점 없음"),
        ]

        reviews = []
        for gear in gears:
            num_reviews = random.randint(1, 4)
            selected_users = random.sample(users, min(num_reviews, len(users)))
            for j, user in enumerate(selected_users):
                title, content, pros, cons = review_templates[j % len(review_templates)]
                review = GearReview(
                    gear_id=gear.id,
                    user_id=user.id,
                    rating=random.randint(3, 5),
                    title=f"{gear.name} - {title}",
                    content=content,
                    pros=pros,
                    cons=cons,
                    usage_duration=random.choice(["1개월", "3개월", "6개월", "1년", "2년"]),
                )
                self.db.add(review)
                reviews.append(review)

            self.db.commit()
            from sqlalchemy import func
            avg = self.db.query(func.avg(GearReview.rating)).filter(GearReview.gear_id == gear.id).scalar()
            gear.average_rating = round(avg, 2) if avg else 0.0
            gear.review_count = len(selected_users)
            self.db.commit()

        logger.info(f"Created {len(reviews)} gear reviews")
        return reviews
