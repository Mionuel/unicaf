// Turns milliseconds to "seconds s" format string
export function formatTime(ms) {
  let totalSeconds = Math.floor(ms / 1000);

  if (totalSeconds < 0)
    totalSeconds = 0;

  return totalSeconds.toString() + " s";
}
