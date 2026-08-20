// Turns milliseconds to "seconds s" format string
export function formatTime(ms) {
  const totalSeconds = Math.floor(ms / 1000);
  return totalSeconds.toString() + " s";
}
