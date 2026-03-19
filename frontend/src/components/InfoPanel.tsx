type InfoPanelProps = {
  title: string;
  items: string[];
  emptyText: string;
};

function InfoPanel({ title, items, emptyText }: InfoPanelProps) {
  return (
    <div className="info-panel">
      <h3 className="info-panel-title">{title}</h3>

      {items.length === 0 ? (
        <p className="info-panel-empty">{emptyText}</p>
      ) : (
        <div className="info-panel-scroll">
          <ul className="info-panel-list">
            {items.map((item, index) => (
              <li key={`${title}-${index}`} className="info-panel-item">
                {item}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default InfoPanel;