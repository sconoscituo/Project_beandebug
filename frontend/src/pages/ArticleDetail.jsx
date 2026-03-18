import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { articlesAPI } from '../api';

const ArticleDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [article, setArticle] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let mounted = true;

    const fetchArticle = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await articlesAPI.getArticle(id);
        if (mounted) setArticle(data);
      } catch (err) {
        if (mounted) setError(err);
      } finally {
        if (mounted) setLoading(false);
      }
    };

    fetchArticle();
    return () => { mounted = false; };
  }, [id]);

  if (loading) return (
    <div style={{ minHeight: '100vh', background: '#0a0a0a', color: '#00ff88', display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: "'Fira Code', monospace" }}>
      {"> DECRYPTING_INTEL_STREAM..."}
    </div>
  );

  if (!article) return (
    <div style={{ minHeight: '100vh', background: '#0a0a0a', color: '#ff5f56', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      {"ERROR: DATA_CORRUPTED_OR_MISSING"}
    </div>
  );

  const isDummyImage = article.thumbnail_url?.startsWith('data:image/gif');

  return (
    <div style={{ minHeight: '100vh', background: '#0a0a0a', color: '#ccc', paddingTop: '100px', paddingBottom: '100px', fontFamily: "'Fira Code', monospace" }}>
      <div style={{ maxWidth: '900px', margin: '0 auto', padding: '2rem', border: '1px solid #333', background: '#111', position: 'relative' }}>
        
        <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '2px', background: '#00ff88' }}></div>

        <button onClick={() => navigate(-1)} style={{ background: 'none', border: '1px solid #00ff88', color: '#00ff88', cursor: 'pointer', padding: '5px 15px', marginBottom: '30px' }}>
          {"[ RETURN_TO_BASE ]"}
        </button>

        <header style={{ marginBottom: '40px', borderBottom: '1px solid #333', paddingBottom: '20px' }}>
          <div style={{ color: '#ff79c6', fontSize: '0.85rem', marginBottom: '10px' }}>
            {`// REPORT_ID: ${article.id} | SLUG: ${article.slug || 'NON_IDENTIFIED'}`}
          </div>
          <h1 style={{ color: '#00ff88', fontSize: '2rem', marginBottom: '15px' }}>
            {article.title}
          </h1>
          
          {/* thumbnail */}
          <div style={{ width: '100%', minHeight: '200px', background: '#000', border: '1px solid #222', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '20px 0' }}>
            {article.thumbnail_url && !isDummyImage ? (
              <img src={article.thumbnail_url} alt="intel" style={{ width: '100%', height: 'auto', opacity: 0.8 }} />
            ) : (
              <div style={{ color: '#333', textAlign: 'center' }}>
                {"[ NO_VISUAL_RECORDS_FOUND ]"}
              </div>
            )}
          </div>

          <div style={{ display: 'flex', gap: '20px', color: '#666', fontSize: '0.8rem' }}>
            <span>{`CATEGORY: ${article.category || 'GENERAL'}`}</span>
            <span>{`VIEWS: ${article.view_count}`}</span>
          </div>
        </header>

        <article style={{ lineHeight: '1.8', color: '#bbb' }}>
          {article.summary && (
            <div style={{ padding: '20px', background: '#1a1a1a', borderLeft: '3px solid #00ff88', marginBottom: '30px', color: '#00ff88', fontSize: '0.95rem' }}>
              {`SUMMARY: ${article.summary}`}
            </div>
          )}
          <div style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-all' }}>
            {article.content}
          </div>
        </article>
      </div>
    </div>
  );
};

export default ArticleDetail;