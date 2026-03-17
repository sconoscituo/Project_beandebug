import React from 'react';

const Pagination = ({ page, totalPages, onPageChange }) => {
  if (totalPages <= 1) return null;

  const getPageNumbers = () => {
    const pages = [];
    const maxVisible = 5;
    let start = Math.max(1, page - Math.floor(maxVisible / 2));
    let end = Math.min(totalPages, start + maxVisible - 1);
    if (end - start + 1 < maxVisible) {
      start = Math.max(1, end - maxVisible + 1);
    }
    for (let i = start; i <= end; i++) pages.push(i);
    return pages;
  };

  const btnStyle = (active) => ({
    padding: '0.5rem 0.85rem',
    background: active ? '#00ff88' : '#1e1e1e',
    color: active ? '#0a0a0a' : '#888',
    border: `1px solid ${active ? '#00ff88' : '#333'}`,
    borderRadius: '6px',
    fontFamily: "'Fira Code', monospace",
    fontSize: '0.8rem',
    cursor: 'pointer',
    transition: 'all 0.2s ease',
    fontWeight: active ? '700' : '400',
  });

  return (
    <div style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      gap: '0.4rem',
      marginTop: '3rem',
      flexWrap: 'wrap',
    }}>
      <button
        onClick={() => onPageChange(1)}
        disabled={page === 1}
        style={{ ...btnStyle(false), opacity: page === 1 ? 0.4 : 1 }}
      >
        {'<<'}
      </button>
      <button
        onClick={() => onPageChange(page - 1)}
        disabled={page === 1}
        style={{ ...btnStyle(false), opacity: page === 1 ? 0.4 : 1 }}
      >
        {'<'}
      </button>
      {getPageNumbers().map((p) => (
        <button key={p} onClick={() => onPageChange(p)} style={btnStyle(p === page)}>
          {p}
        </button>
      ))}
      <button
        onClick={() => onPageChange(page + 1)}
        disabled={page === totalPages}
        style={{ ...btnStyle(false), opacity: page === totalPages ? 0.4 : 1 }}
      >
        {'>'}
      </button>
      <button
        onClick={() => onPageChange(totalPages)}
        disabled={page === totalPages}
        style={{ ...btnStyle(false), opacity: page === totalPages ? 0.4 : 1 }}
      >
        {'>>'}
      </button>
      <span style={{
        fontFamily: "'Fira Code', monospace",
        fontSize: '0.75rem',
        color: '#666',
        marginLeft: '0.5rem',
      }}>
        {page} / {totalPages}
      </span>
    </div>
  );
};

export default Pagination;
