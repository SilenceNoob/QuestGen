// 全局变量
let currentQuestions = [];
let userAnswers = {};
let currentQuestionIndex = 0;

// 工具函数
function showMessage(message, type = 'info') {
    // 移除现有消息
    const existingMessage = document.querySelector('.message');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    // 创建新消息
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.innerHTML = `
        <span class="message-text">${message}</span>
        <button class="message-close" onclick="this.parentElement.remove()">&times;</button>
    `;
    
    document.body.appendChild(messageDiv);
    
    // 自动移除消息
    setTimeout(() => {
        if (messageDiv.parentElement) {
            messageDiv.remove();
        }
    }, 5000);
}

function showModal(title, message, onConfirm, onCancel) {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content">
            <h3>${title}</h3>
            <p>${message}</p>
            <div class="modal-actions">
                <button class="btn btn-secondary" onclick="closeModal()">取消</button>
                <button class="btn btn-primary" onclick="confirmModal()">确认</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // 设置回调函数
    window.confirmModal = () => {
        closeModal();
        if (onConfirm) onConfirm();
    };
    
    window.closeModal = () => {
        modal.remove();
        if (onCancel) onCancel();
    };
    
    // 点击背景关闭
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeModal();
        }
    });
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function updateProgress() {
    const totalQuestions = currentQuestions.length;
    const answeredQuestions = Object.keys(userAnswers).length;
    const percentage = totalQuestions > 0 ? (answeredQuestions / totalQuestions) * 100 : 0;
    
    const progressFill = document.querySelector('.progress-fill');
    const progressText = document.querySelector('.progress-summary span');
    
    if (progressFill) {
        progressFill.style.width = `${percentage}%`;
    }
    
    if (progressText) {
        progressText.textContent = `已完成 ${answeredQuestions} / ${totalQuestions} 题 (${Math.round(percentage)}%)`;
    }
    
    // 更新每个题目的完成状态
    document.querySelectorAll('.question-card').forEach((card, index) => {
        const indicator = card.querySelector('.progress-indicator');
        if (indicator) {
            const questionId = `q${index + 1}`;
            if (userAnswers[questionId]) {
                indicator.textContent = '已完成';
                indicator.className = 'progress-indicator completed';
            } else {
                indicator.textContent = '未完成';
                indicator.className = 'progress-indicator';
            }
        }
    });
}

function saveProgress() {
    if (typeof(Storage) !== "undefined") {
        localStorage.setItem('quiz_answers', JSON.stringify(userAnswers));
        localStorage.setItem('quiz_timestamp', new Date().toISOString());
    }
}

function loadProgress() {
    if (typeof(Storage) !== "undefined") {
        const savedAnswers = localStorage.getItem('quiz_answers');
        if (savedAnswers) {
            try {
                userAnswers = JSON.parse(savedAnswers);
                // 恢复答案到表单
                Object.keys(userAnswers).forEach(questionId => {
                    const answer = userAnswers[questionId];
                    if (Array.isArray(answer)) {
                        // 多选题
                        answer.forEach(value => {
                            const input = document.querySelector(`input[name="${questionId}"][value="${value}"]`);
                            if (input) input.checked = true;
                        });
                    } else {
                        // 单选题或判断题
                        const input = document.querySelector(`input[name="${questionId}"][value="${answer}"]`);
                        if (input) input.checked = true;
                    }
                });
                updateProgress();
                showMessage('已恢复之前的答题进度', 'info');
            } catch (e) {
                console.error('恢复进度失败:', e);
            }
        }
    }
}

function clearProgress() {
    if (typeof(Storage) !== "undefined") {
        localStorage.removeItem('quiz_answers');
        localStorage.removeItem('quiz_timestamp');
    }
    userAnswers = {};
    updateProgress();
}

// 文件上传相关函数
function initFileUpload() {
    const fileInput = document.getElementById('file-input');
    const uploadArea = document.querySelector('.file-upload-area');
    const fileInfo = document.querySelector('.file-info');
    
    if (!fileInput || !uploadArea) return;
    
    // 点击上传区域触发文件选择
    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });
    
    // 文件选择处理
    fileInput.addEventListener('change', handleFileSelect);
    
    // 拖拽上传
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('drag-over');
    });
    
    uploadArea.addEventListener('dragleave', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            handleFileSelect({ target: { files: files } });
        }
    });
}

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    // 检查文件类型
    const allowedTypes = ['.txt', '.docx', '.pdf', '.md'];
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
    
    if (!allowedTypes.includes(fileExtension)) {
        showMessage('请选择支持的文件格式：TXT、DOCX、PDF、MD', 'error');
        return;
    }
    
    // 检查文件大小（10MB限制）
    if (file.size > 10 * 1024 * 1024) {
        showMessage('文件大小不能超过10MB', 'error');
        return;
    }
    
    // 显示文件信息
    displayFileInfo(file);
    
    // 上传文件
    uploadFile(file);
}

function displayFileInfo(file) {
    const fileInfo = document.querySelector('.file-info');
    if (fileInfo) {
        fileInfo.style.display = 'flex';
        fileInfo.querySelector('.file-name').textContent = file.name;
        fileInfo.querySelector('.file-size').textContent = formatFileSize(file.size);
    }
}

function removeFile() {
    const fileInput = document.getElementById('file-input');
    const fileInfo = document.querySelector('.file-info');
    const documentInfo = document.querySelector('.document-info');
    
    if (fileInput) fileInput.value = '';
    if (fileInfo) fileInfo.style.display = 'none';
    if (documentInfo) documentInfo.style.display = 'none';
    
    showMessage('文件已移除', 'info');
}

function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    // 显示上传进度
    showMessage('正在上传文件...', 'info');
    
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage('文件上传成功！', 'success');
            displayDocumentInfo(data.document_info);
        } else {
            showMessage(data.error || '文件上传失败', 'error');
        }
    })
    .catch(error => {
        console.error('上传错误:', error);
        showMessage('文件上传失败，请重试', 'error');
    });
}

function displayDocumentInfo(info) {
    const documentInfo = document.querySelector('.document-info');
    if (!documentInfo) return;
    
    documentInfo.style.display = 'block';
    
    // 更新文档信息
    const infoItems = documentInfo.querySelectorAll('.info-item span');
    if (infoItems.length >= 4) {
        infoItems[0].textContent = info.filename;
        infoItems[1].textContent = info.file_type.toUpperCase();
        infoItems[2].textContent = formatFileSize(info.file_size);
        infoItems[3].textContent = `约 ${info.word_count} 字`;
    }
}

function updateTotalCount() {
    const singleCount = parseInt(document.getElementById('single-count').value) || 0;
    const multipleCount = parseInt(document.getElementById('multiple-count').value) || 0;
    const judgeCount = parseInt(document.getElementById('judge-count').value) || 0;
    const total = singleCount + multipleCount + judgeCount;
    
    const totalElement = document.querySelector('.total-count');
    if (totalElement) {
        totalElement.innerHTML = `总计：<strong>${total}</strong> 道题目`;
    }
}

function generateQuestions() {
    const singleCount = parseInt(document.getElementById('single-count').value) || 0;
    const multipleCount = parseInt(document.getElementById('multiple-count').value) || 0;
    const judgeCount = parseInt(document.getElementById('judge-count').value) || 0;
    
    if (singleCount + multipleCount + judgeCount === 0) {
        showMessage('请至少设置一种题型的数量', 'error');
        return;
    }
    
    const generateBtn = document.getElementById('generate-btn');
    if (generateBtn) {
        generateBtn.disabled = true;
        generateBtn.innerHTML = '<span class="loading-spinner">⟳</span> 正在生成题目...';
    }
    
    const requestData = {
        single_choice: singleCount,
        multiple_choice: multipleCount,
        true_false: judgeCount
    };
    
    fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage('题目生成成功！正在跳转到答题页面...', 'success');
            setTimeout(() => {
                window.location.href = '/quiz';
            }, 1500);
        } else {
            showMessage(data.error || '题目生成失败', 'error');
        }
    })
    .catch(error => {
        console.error('生成错误:', error);
        showMessage('题目生成失败，请重试', 'error');
    })
    .finally(() => {
        if (generateBtn) {
            generateBtn.disabled = false;
            generateBtn.innerHTML = '🚀 开始生成题目';
        }
    });
}

// 答题相关函数
function initQuiz() {
    // 获取题目数据
    const questionsData = document.getElementById('questions-data');
    if (questionsData) {
        try {
            currentQuestions = JSON.parse(questionsData.textContent);
        } catch (e) {
            console.error('解析题目数据失败:', e);
        }
    }
    
    // 绑定答案选择事件
    document.querySelectorAll('input[type="radio"], input[type="checkbox"]').forEach(input => {
        input.addEventListener('change', handleAnswerChange);
    });
    
    // 加载之前的进度
    loadProgress();
    
    // 初始化进度显示
    updateProgress();
}

function handleAnswerChange(event) {
    const input = event.target;
    const questionId = input.name;
    const questionType = input.type;
    
    if (questionType === 'radio') {
        // 单选题或判断题
        userAnswers[questionId] = input.value;
    } else if (questionType === 'checkbox') {
        // 多选题
        if (!userAnswers[questionId]) {
            userAnswers[questionId] = [];
        }
        
        if (input.checked) {
            if (!userAnswers[questionId].includes(input.value)) {
                userAnswers[questionId].push(input.value);
            }
        } else {
            userAnswers[questionId] = userAnswers[questionId].filter(val => val !== input.value);
            if (userAnswers[questionId].length === 0) {
                delete userAnswers[questionId];
            }
        }
    }
    
    // 保存进度并更新显示
    saveProgress();
    updateProgress();
}

function submitQuiz() {
    const totalQuestions = currentQuestions.length;
    const answeredQuestions = Object.keys(userAnswers).length;
    
    if (answeredQuestions < totalQuestions) {
        const unanswered = totalQuestions - answeredQuestions;
        showModal(
            '确认提交',
            `您还有 ${unanswered} 道题目未完成，确定要提交答案吗？`,
            () => doSubmitQuiz(),
            null
        );
    } else {
        showModal(
            '确认提交',
            '确定要提交答案吗？提交后将无法修改。',
            () => doSubmitQuiz(),
            null
        );
    }
}

function doSubmitQuiz() {
    const submitBtn = document.getElementById('submit-btn');
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="loading-spinner">⟳</span> 正在提交...';
    }
    
    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ answers: userAnswers })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage('答案提交成功！正在跳转到结果页面...', 'success');
            clearProgress(); // 清除本地进度
            setTimeout(() => {
                window.location.href = '/result';
            }, 1500);
        } else {
            showMessage(data.error || '提交失败', 'error');
        }
    })
    .catch(error => {
        console.error('提交错误:', error);
        showMessage('提交失败，请重试', 'error');
    })
    .finally(() => {
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = '📝 提交答案';
        }
    });
}

function saveAndExit() {
    showModal(
        '保存并退出',
        '您的答题进度将被保存，下次访问时可以继续答题。',
        () => {
            saveProgress();
            showMessage('进度已保存', 'success');
            setTimeout(() => {
                window.location.href = '/';
            }, 1000);
        },
        null
    );
}

// 结果页面相关函数
function initResult() {
    // 初始化分数圆环动画
    const scoreCircle = document.querySelector('.score-circle');
    if (scoreCircle) {
        const percentage = parseFloat(scoreCircle.dataset.percentage) || 0;
        setTimeout(() => {
            scoreCircle.style.setProperty('--percentage', percentage);
        }, 500);
    }
    
    // 初始化筛选功能
    initResultFilter();
}

function initResultFilter() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const resultCards = document.querySelectorAll('.result-card');
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // 更新活动标签
            tabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // 筛选结果
            const filter = btn.dataset.filter;
            resultCards.forEach(card => {
                if (filter === 'all' || card.classList.contains(filter)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
}

function printResults() {
    window.print();
}

function restartQuiz() {
    showModal(
        '重新开始',
        '确定要重新开始吗？当前的答题结果将被清除。',
        () => {
            fetch('/restart', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    clearProgress();
                    showMessage('正在重新开始...', 'info');
                    setTimeout(() => {
                        window.location.href = '/';
                    }, 1000);
                } else {
                    showMessage('操作失败，请重试', 'error');
                }
            })
            .catch(error => {
                console.error('重启错误:', error);
                showMessage('操作失败，请重试', 'error');
            });
        },
        null
    );
}

// 页面初始化
document.addEventListener('DOMContentLoaded', function() {
    // 根据页面类型初始化不同功能
    const currentPage = window.location.pathname;
    
    if (currentPage === '/upload') {
        initFileUpload();
        
        // 绑定题目数量变化事件
        ['single-count', 'multiple-count', 'judge-count'].forEach(id => {
            const input = document.getElementById(id);
            if (input) {
                input.addEventListener('input', updateTotalCount);
            }
        });
        
        // 初始化总数显示
        updateTotalCount();
        
    } else if (currentPage === '/quiz') {
        initQuiz();
        
    } else if (currentPage === '/result') {
        initResult();
    }
    
    // 全局键盘快捷键
    document.addEventListener('keydown', function(e) {
        // Ctrl+S 保存进度（仅在答题页面）
        if (e.ctrlKey && e.key === 's' && currentPage === '/quiz') {
            e.preventDefault();
            saveProgress();
            showMessage('进度已保存', 'success');
        }
        
        // ESC 关闭模态框
        if (e.key === 'Escape') {
            const modal = document.querySelector('.modal');
            if (modal && window.closeModal) {
                window.closeModal();
            }
        }
    });
});

// 导出函数供HTML调用
window.removeFile = removeFile;
window.generateQuestions = generateQuestions;
window.submitQuiz = submitQuiz;
window.saveAndExit = saveAndExit;
window.printResults = printResults;
window.restartQuiz = restartQuiz;