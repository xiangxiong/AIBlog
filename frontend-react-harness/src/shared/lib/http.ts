export function fakeRequest<T>(payload: T, delay = 300): Promise<T> {
  return new Promise((resolve) => {
    window.setTimeout(() => {
      resolve(payload);
    }, delay);
  });
}
