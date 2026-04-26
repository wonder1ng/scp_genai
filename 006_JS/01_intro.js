function leftTriangle(lines) {
  for (let i = 1; i <= lines; i++) {
    console.log("*".repeat(i));
  }
}
function leftReverseTriangle(lines) {
  for (let i = lines; i != 0; i--) {
    console.log("*".repeat(i));
  }
}
function rightTriangle(lines) {
  for (let i = 1; i <= lines; i++) {
    console.log(" ".repeat(lines - i) + "*".repeat(i));
  }
}
function rightReverseTriangle(lines) {
  for (let i = lines; i != 0; i--) {
    console.log(" ".repeat(lines - i) + "*".repeat(i));
  }
}
function isoscelesTriangle(lines) {
  for (let i = 1; i <= lines; i++) {
    console.log(" ".repeat(lines - i) + "*".repeat(i * 2));
  }
}
function rhombus(lines) {
  let odd = lines % 2;
  let half = (lines + odd) / 2;
  for (let i = 1; i <= lines; i++) {
    console.log(
      " ".repeat(i > half ? (odd ? i - half : i - half - 1) : half - i) +
        "*".repeat((i > half ? lines - i + 1 : i) * 2),
    );
  }
}
leftTriangle(5);
leftReverseTriangle(5);
rightTriangle(5);
rightReverseTriangle(5);
isoscelesTriangle(5);
rhombus(5);
rhombus(6);
