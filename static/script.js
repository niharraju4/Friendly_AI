
let canvas = document.getElementById("canvas");
let ctx = canvas.getContext("2d");
let points = [];
let numPoints = 300;  // Increased number of points

// Initialize canvas size
function resizeCanvas() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}
resizeCanvas();
window.addEventListener("resize", resizeCanvas);

// Generate random points with colors
for (let i = 0; i < numPoints; i++) {
  points.push({
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height,
    vx: (Math.random() - 0.5) * 4,  // Increased speed
    vy: (Math.random() - 0.5) * 4,  // Increased speed
    color: `rgb(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)})`
  });
}

// Animation loop
function animate() {
  requestAnimationFrame(animate);
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Move and draw points
  points.forEach(point => {
    point.x += point.vx;
    point.y += point.vy;
    if (point.x < 0 || point.x > canvas.width) point.vx = -point.vx;
    if (point.y < 0 || point.y > canvas.height) point.vy = -point.vy;

    // Draw the point
    ctx.fillStyle = point.color;
    ctx.beginPath();
    ctx.arc(point.x, point.y, 2, 0, Math.PI * 2);
    ctx.fill();
  });

  // Draw lines between close points
  for (let i = 0; i < points.length; i++) {
    for (let j = i + 1; j < points.length; j++) {
      let dx = points[i].x - points[j].x;
      let dy = points[i].y - points[j].y;
      let dist = Math.sqrt(dx * dx + dy * dy);
      if (dist < 100) {
        ctx.strokeStyle = points[i].color;
        ctx.lineWidth = 0.5;
        ctx.beginPath();
        ctx.moveTo(points[i].x, points[i].y);
        ctx.lineTo(points[j].x, points[j].y);
        ctx.stroke();
      }
    }
  }
}
animate();
