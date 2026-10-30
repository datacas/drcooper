export interface Price {
  amount: number;
  currency: string;
}

export function formatPrice(price: Price): string {
  return `${price.amount.toFixed(2)} ${price.currency}`;
}
