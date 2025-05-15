// Document Viewer and Annotation JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Toggle annotation tools
    const toggleAnnotationBtn = document.getElementById('toggleAnnotation');
    const annotationTools = document.getElementById('annotationTools');
    
    if (toggleAnnotationBtn && annotationTools) {
        toggleAnnotationBtn.addEventListener('click', function() {
            if (annotationTools.style.display === 'none') {
                annotationTools.style.display = 'block';
                toggleAnnotationBtn.innerHTML = '<i class="bi bi-x"></i> Fechar Anotações';
                initializeAnnotationCanvas();
            } else {
                annotationTools.style.display = 'none';
                toggleAnnotationBtn.innerHTML = '<i class="bi bi-pencil"></i> Anotar Documento';
            }
        });
    }
    
    // Initialize annotation canvas
    function initializeAnnotationCanvas() {
        const documentImage = document.getElementById('documentImage');
        if (!documentImage) return;
        
        // Create canvas if it doesn't exist
        let canvas = document.getElementById('annotationCanvas');
        if (!canvas) {
            canvas = document.createElement('canvas');
            canvas.id = 'annotationCanvas';
            documentImage.parentNode.appendChild(canvas);
            
            // Position canvas over the image
            positionCanvas();
            
            // Handle window resize
            window.addEventListener('resize', positionCanvas);
        }
        
        function positionCanvas() {
            const rect = documentImage.getBoundingClientRect();
            canvas.width = rect.width;
            canvas.height = rect.height;
            canvas.style.position = 'absolute';
            canvas.style.left = `${rect.left}px`;
            canvas.style.top = `${rect.top}px`;
            canvas.style.zIndex = '10';
        }
        
        // Drawing functionality
        const ctx = canvas.getContext('2d');
        let isDrawing = false;
        let lastX = 0;
        let lastY = 0;
        let currentTool = 'pen';
        let currentColor = 'red';
        let lineWidth = 2;
        
        // Load existing annotations if available
        const clientAnnotations = document.getElementById('clientAnnotationsData');
        if (clientAnnotations && clientAnnotations.value) {
            try {
                const img = new Image();
                img.onload = function() {
                    ctx.drawImage(img, 0, 0);
                };
                img.src = clientAnnotations.value;
            } catch (e) {
                console.error('Error loading annotations:', e);
            }
        }
        
        // Tool selection
        const toolButtons = document.querySelectorAll('[data-tool]');
        toolButtons.forEach(button => {
            button.addEventListener('click', function() {
                currentTool = this.getAttribute('data-tool');
                toolButtons.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');
                
                // Adjust line width based on tool
                if (currentTool === 'pen') {
                    lineWidth = 2;
                } else if (currentTool === 'highlighter') {
                    lineWidth = 10;
                    ctx.globalAlpha = 0.3;
                } else {
                    lineWidth = 20;
                    ctx.globalAlpha = 1;
                }
            });
        });
        
        // Color selection
        const colorButtons = document.querySelectorAll('[data-color]');
        colorButtons.forEach(button => {
            button.addEventListener('click', function() {
                currentColor = this.getAttribute('data-color');
                colorButtons.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');
            });
        });
        
        // Drawing events
        canvas.addEventListener('mousedown', startDrawing);
        canvas.addEventListener('touchstart', handleTouchStart);
        canvas.addEventListener('mousemove', draw);
        canvas.addEventListener('touchmove', handleTouchMove);
        canvas.addEventListener('mouseup', stopDrawing);
        canvas.addEventListener('touchend', stopDrawing);
        canvas.addEventListener('mouseout', stopDrawing);
        
        function startDrawing(e) {
            isDrawing = true;
            [lastX, lastY] = [e.offsetX, e.offsetY];
        }
        
        function handleTouchStart(e) {
            e.preventDefault();
            const touch = e.touches[0];
            const rect = canvas.getBoundingClientRect();
            const offsetX = touch.clientX - rect.left;
            const offsetY = touch.clientY - rect.top;
            
            isDrawing = true;
            [lastX, lastY] = [offsetX, offsetY];
        }
        
        function draw(e) {
            if (!isDrawing) return;
            
            ctx.beginPath();
            ctx.moveTo(lastX, lastY);
            ctx.lineTo(e.offsetX, e.offsetY);
            ctx.strokeStyle = currentColor;
            ctx.lineWidth = lineWidth;
            ctx.lineCap = 'round';
            
            if (currentTool === 'eraser') {
                ctx.globalCompositeOperation = 'destination-out';
            } else {
                ctx.globalCompositeOperation = 'source-over';
            }
            
            ctx.stroke();
            [lastX, lastY] = [e.offsetX, e.offsetY];
        }
        
        function handleTouchMove(e) {
            e.preventDefault();
            if (!isDrawing) return;
            
            const touch = e.touches[0];
            const rect = canvas.getBoundingClientRect();
            const offsetX = touch.clientX - rect.left;
            const offsetY = touch.clientY - rect.top;
            
            ctx.beginPath();
            ctx.moveTo(lastX, lastY);
            ctx.lineTo(offsetX, offsetY);
            ctx.strokeStyle = currentColor;
            ctx.lineWidth = lineWidth;
            ctx.lineCap = 'round';
            
            if (currentTool === 'eraser') {
                ctx.globalCompositeOperation = 'destination-out';
            } else {
                ctx.globalCompositeOperation = 'source-over';
            }
            
            ctx.stroke();
            [lastX, lastY] = [offsetX, offsetY];
        }
        
        function stopDrawing() {
            isDrawing = false;
        }
        
        // Save annotations
        const saveBtn = document.getElementById('saveAnnotations');
        if (saveBtn) {
            saveBtn.addEventListener('click', function() {
                const dataURL = canvas.toDataURL();
                
                // Send to server using fetch API
                const documentId = window.location.pathname.split('/').pop();
                fetch(`/document/annotate/${documentId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        annotation_data: dataURL
                    }),
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Anotações salvas com sucesso!');
                    } else {
                        alert('Erro ao salvar anotações: ' + data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Erro ao salvar anotações. Por favor, tente novamente.');
                });
            });
        }
        
        // Clear annotations
        const clearBtn = document.getElementById('clearAnnotations');
        if (clearBtn) {
            clearBtn.addEventListener('click', function() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
            });
        }
    }
});
