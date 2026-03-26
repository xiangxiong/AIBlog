export type DashboardMetric = {
  label: string;
  value: string;
  trend: string;
};

export type DashboardTodo = {
  title: string;
  detail: string;
};

export type DashboardSnapshot = {
  title: string;
  subtitle: string;
  metrics: DashboardMetric[];
  todos: DashboardTodo[];
};
