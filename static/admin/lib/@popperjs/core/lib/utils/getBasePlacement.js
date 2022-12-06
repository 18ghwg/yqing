import { auto } from "../enums.d.ts";
export default function getBasePlacement(placement) {
  return placement.split('-')[0];
}