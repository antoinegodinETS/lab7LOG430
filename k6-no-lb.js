import http from 'k6/http';
import { check } from 'k6';

export const options = {
  vus: 20,
  duration: '10s',
};

export default function () {
  const res = http.get('http://localhost:8004/panier/1');
  check(res, { 'status is OK': (r) => r.status < 500 });

}
