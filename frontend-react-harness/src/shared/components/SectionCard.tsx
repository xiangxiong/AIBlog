type SectionCardProps = {
  title: string;
  summary: string;
  bullets: string[];
};

export function SectionCard({ title, summary, bullets }: SectionCardProps) {
  return (
    <article className="section-card">
      <h2>{title}</h2>
      <p>{summary}</p>
      <ul>
        {bullets.map((bullet) => (
          <li key={bullet}>{bullet}</li>
        ))}
      </ul>
    </article>
  );
}
