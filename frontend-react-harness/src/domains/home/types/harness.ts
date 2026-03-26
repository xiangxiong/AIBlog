export type PlaybookSection = {
  title: string;
  summary: string;
  bullets: string[];
};

export type HarnessPlaybook = {
  heroTitle: string;
  heroSummary: string;
  metrics: Array<{
    label: string;
    value: string;
    detail: string;
  }>;
  sections: PlaybookSection[];
  footerNote: string;
};
