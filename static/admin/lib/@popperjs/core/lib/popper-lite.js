import { popperGenerator, detectOverflow } from "./createPopper.d.ts";
import eventListeners from "./modifiers/eventListeners.d.ts";
import popperOffsets from "./modifiers/popperOffsets.d.ts";
import computeStyles from "./modifiers/computeStyles.d.ts";
import applyStyles from "./modifiers/applyStyles.d.ts";
var defaultModifiers = [eventListeners, popperOffsets, computeStyles, applyStyles];
var createPopper = /*#__PURE__*/popperGenerator({
  defaultModifiers: defaultModifiers
}); // eslint-disable-next-line import/no-unused-modules

export { createPopper, popperGenerator, defaultModifiers, detectOverflow };