import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const samplePosts = [
  { id: 1, author: 'barista_kim', title: '오늘의 V60 추출 기록', content: '에티오피아 예가체프 코체레로 V60 추출했습니다. 93도, 18g:300ml, 2분 40초. 플로럴한 향이 정말 좋았어요!', likes: 42, comments: 8, time: '2시간 전', tag: '추출 기록' },
  { id: 2, author: 'coffee_lee', title: 'Comandante C40 vs Timemore C2 비교 후기', content: '두 달간 두 그라인더를 번갈아 사용해봤습니다. 결론부터 말하면, 분쇄 균일도에서 확실한 차이가 있습니다.', likes: 87, comments: 23, time: '3시간 전', tag: '장비 리뷰' },
  { id: 3, author: 'roaster_park', title: '홈로스팅 첫 도전! (feat. 수망)', content: '수망으로 에티오피아 생두를 볶아봤는데, 1차 크랙 후 1분 30초에 배출했습니다. 연기가 장난 아니네요 ㅋㅋ', likes: 56, comments: 15, time: '5시간 전', tag: '홈로스팅' },
  { id: 4, author: 'brew_choi', title: '에어로프레스 대회 준비 레시피 공유', content: '대회 준비하면서 만든 레시피입니다. 16g, 80도, 230ml, 인버트, 2분 30초 스티핑. 피드백 부탁드려요!', likes: 134, comments: 31, time: '6시간 전', tag: '레시피 공유' },
  { id: 5, author: 'cafe_jung', title: '서울 성수동 카페 투어 후기', content: 'Mano Coffee, Anthracite, Mesh Coffee 3곳을 다녀왔습니다. 각각의 시그니처 메뉴와 분위기를 공유합니다.', likes: 98, comments: 19, time: '8시간 전', tag: '카페 투어' },
  { id: 6, author: 'barista_kim', title: '물 TDS 실험 결과 공유', content: '삼다수, 브리타, Third Wave Water 세 가지로 같은 원두 추출 비교. TDS 150ppm이 역시 최적이었습니다.', likes: 76, comments: 12, time: '10시간 전', tag: '실험/연구' },
  { id: 7, author: 'coffee_lee', title: '콜드브루 원액 활용법 5가지', content: '콜드브루 원액으로 라떼, 토닉, 아포가토, 칵테일, 디저트 소스까지! 레시피 공유합니다.', likes: 112, comments: 27, time: '12시간 전', tag: '레시피 공유' },
  { id: 8, author: 'roaster_park', title: '파나마 게이샤 커핑 노트', content: 'La Esmeralda 게이샤를 커핑했습니다. SCA 점수 92점. 재스민, 열대과일, 실키한 마우스필. 역시 게이샤...', likes: 145, comments: 34, time: '1일 전', tag: '커핑 노트' },
  { id: 9, author: 'brew_choi', title: '프렌치프레스로 에스프레소 농도 만들기', content: '프렌치프레스에 미세 분쇄 + 1:4 비율로 진한 커피를 추출하는 방법을 시도해봤습니다.', likes: 63, comments: 16, time: '1일 전', tag: '실험/연구' },
  { id: 10, author: 'cafe_jung', title: '카페 창업 3개월 후기', content: '카페를 오픈한 지 3개월이 되었습니다. 매출, 원가, 힘들었던 점, 보람 있었던 점을 솔직하게 공유합니다.', likes: 203, comments: 45, time: '1일 전', tag: '카페 운영' },
  { id: 11, author: 'barista_kim', title: '라떼아트 연습 30일 챌린지 결과', content: '매일 20잔씩 라떼아트 연습한 결과를 공유합니다. 1일차 vs 30일차 비교 사진 포함!', likes: 178, comments: 38, time: '2일 전', tag: '라떼아트' },
  { id: 12, author: 'coffee_lee', title: '겨울 시즌 메뉴 추천', content: '따뜻한 겨울 커피 메뉴 5가지: 스파이스 라떼, 핫 토디, 아이리쉬 커피, 카페 비엔나, 진저 에스프레소', likes: 89, comments: 14, time: '2일 전', tag: '레시피 공유' },
  { id: 13, author: 'roaster_park', title: '생두 보관 실험 6개월 결과', content: '진공팩 vs 그레인프로 vs 일반 봉투에 보관한 에티오피아 생두의 6개월 후 맛 변화를 비교했습니다.', likes: 95, comments: 21, time: '2일 전', tag: '실험/연구' },
  { id: 14, author: 'brew_choi', title: '칼리타 웨이브 vs V60 블라인드 테스트', content: '5명이 블라인드 테스트한 결과, 의외로 칼리타 웨이브가 3:2로 선호되었습니다. 균일한 추출이 비결?', likes: 121, comments: 29, time: '3일 전', tag: '실험/연구' },
  { id: 15, author: 'cafe_jung', title: '인스타 감성 카페 인테리어 팁', content: '카페 인테리어에서 가장 중요한 3가지: 조명, 좌석 배치, 포토존. 실제 적용 사례를 공유합니다.', likes: 156, comments: 33, time: '3일 전', tag: '카페 운영' },
];

const tags = ['전체', '추출 기록', '레시피 공유', '장비 리뷰', '커핑 노트', '실험/연구', '카페 투어', '카페 운영', '홈로스팅', '라떼아트'];

const tagColors = {
  '추출 기록': '#00ff88',
  '레시피 공유': '#8be9fd',
  '장비 리뷰': '#ffb86c',
  '커핑 노트': '#ff79c6',
  '실험/연구': '#bd93f9',
  '카페 투어': '#f1fa8c',
  '카페 운영': '#ff5f56',
  '홈로스팅': '#ffb86c',
  '라떼아트': '#8be9fd',
};

const Community = () => {
  const [filter, setFilter] = useState('전체');
  const [page, setPage] = useState(1);
  const PAGE_SIZE = 8;

  const filtered = filter === '전체' ? samplePosts : samplePosts.filter(p => p.tag === filter);
  const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  const displayed = filtered.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE);

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%)',
      paddingTop: '120px',
      paddingBottom: '4rem',
      fontFamily: "'Fira Code', monospace",
    }}>
      <div style={{ maxWidth: '900px', margin: '0 auto', padding: '0 2rem' }}>
        <div style={{ marginBottom: '2rem' }}>
          <div style={{ color: '#888', fontSize: '0.9rem', marginBottom: '0.5rem' }}>
            <span style={{ color: '#00ff88' }}>$</span> join ./community --channel=all
          </div>
          <h1 style={{ fontSize: '2.5rem', color: '#00ff88', marginBottom: '0.5rem' }}>
            Community
          </h1>
          <p style={{ color: '#666', fontSize: '0.9rem' }}>
            // 커피 러버들의 이야기를 나누는 공간
          </p>
        </div>

        <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '2rem', overflowX: 'auto', paddingBottom: '0.5rem', scrollbarWidth: 'none' }}>
          {tags.map(tag => (
            <button key={tag} onClick={() => { setFilter(tag); setPage(1); }}
              style={{
                padding: '0.5rem 1rem',
                background: filter === tag ? '#00ff88' : '#1e1e1e',
                color: filter === tag ? '#0a0a0a' : '#888',
                border: `1px solid ${filter === tag ? '#00ff88' : '#333'}`,
                borderRadius: '6px', fontSize: '0.8rem', cursor: 'pointer',
                whiteSpace: 'nowrap', transition: 'all 0.2s ease',
                fontFamily: "'Fira Code', monospace",
              }}
            >
              {tag}
            </button>
          ))}
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {displayed.map(post => (
            <div key={post.id}
              style={{
                background: '#1e1e1e', borderRadius: '12px',
                border: '1px solid #333', overflow: 'hidden',
                transition: 'all 0.3s ease', cursor: 'pointer',
              }}
              onMouseOver={(e) => { e.currentTarget.style.borderColor = '#00ff88'; }}
              onMouseOut={(e) => { e.currentTarget.style.borderColor = '#333'; }}
            >
              <div style={{
                background: '#2d2d2d', padding: '10px 14px',
                display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                borderBottom: '1px solid #333',
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#ff5f56' }} />
                  <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#ffbd2e' }} />
                  <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#27ca3f' }} />
                  <span style={{ marginLeft: '8px', color: '#888', fontSize: '0.75rem' }}>
                    @{post.author}
                  </span>
                  <span style={{ color: '#555', fontSize: '0.7rem' }}>
                    {post.time}
                  </span>
                </div>
                <span style={{
                  padding: '2px 8px', borderRadius: '4px', fontSize: '0.65rem', fontWeight: '600',
                  background: tagColors[post.tag] || '#888', color: '#0a0a0a',
                }}>
                  {post.tag}
                </span>
              </div>

              <div style={{ padding: '1.25rem' }}>
                <h3 style={{ fontSize: '1.05rem', color: '#00ff88', marginBottom: '0.75rem' }}>
                  {post.title}
                </h3>
                <p style={{
                  fontSize: '0.85rem', color: '#999', lineHeight: 1.6,
                  marginBottom: '1rem',
                  overflow: 'hidden', textOverflow: 'ellipsis',
                  display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical',
                }}>
                  {post.content}
                </p>
                <div style={{
                  display: 'flex', gap: '1.5rem', fontSize: '0.8rem',
                  paddingTop: '0.75rem', borderTop: '1px solid #333',
                }}>
                  <span style={{ color: '#ff79c6' }}>♥ {post.likes}</span>
                  <span style={{ color: '#8be9fd' }}>💬 {post.comments}</span>
                  <span style={{ color: '#666', marginLeft: 'auto' }}>[ READ_MORE ]</span>
                </div>
              </div>
            </div>
          ))}
        </div>

        {totalPages > 1 && (
          <div style={{
            display: 'flex', justifyContent: 'center', gap: '0.4rem',
            marginTop: '3rem', flexWrap: 'wrap',
          }}>
            {Array.from({ length: totalPages }, (_, i) => i + 1).map(p => (
              <button key={p} onClick={() => { setPage(p); window.scrollTo({ top: 0, behavior: 'smooth' }); }}
                style={{
                  padding: '0.5rem 0.85rem',
                  background: p === page ? '#00ff88' : '#1e1e1e',
                  color: p === page ? '#0a0a0a' : '#888',
                  border: `1px solid ${p === page ? '#00ff88' : '#333'}`,
                  borderRadius: '6px', fontSize: '0.8rem', cursor: 'pointer',
                  fontFamily: "'Fira Code', monospace",
                  fontWeight: p === page ? '700' : '400',
                }}
              >
                {p}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Community;
