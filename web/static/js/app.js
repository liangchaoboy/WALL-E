// 全局状态
let mediaRecorder;
let audioChunks = [];
let isRecording = false;

// DOM 元素
const tabs = document.querySelectorAll('.tab');
const tabContents = document.querySelectorAll('.tab-content');
const textInput = document.getElementById('textInput');
const recordBtn = document.getElementById('recordBtn');
const recordingStatus = document.getElementById('recordingStatus');
const aiProviderSelect = document.getElementById('aiProvider');
const mapProviderSelect = document.getElementById('mapProvider');
const submitBtn = document.getElementById('submitBtn');
const resultSection = document.getElementById('resultSection');
const resultContent = document.getElementById('resultContent');
const loadingSection = document.getElementById('loadingSection');
const loadingText = document.getElementById('loadingText');

// 当前输入类型
let currentInputType = 'text';

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    initRecording();
    initSubmit();
});

// 初始化标签页
function initTabs() {
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const tabName = tab.dataset.tab;
            
            // 切换标签页样式
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            // 切换内容
            tabContents.forEach(content => content.classList.remove('active'));
            document.getElementById(`${tabName}-tab`).classList.add('active');
            
            // 设置当前输入类型
            currentInputType = tabName === 'text' ? 'text' : 'audio';
        });
    });
}

// 初始化录音
function initRecording() {
    recordBtn.addEventListener('click', toggleRecording);
}

// 切换录音状态
async function toggleRecording() {
    if (!isRecording) {
        await startRecording();
    } else {
        stopRecording();
    }
}

// 开始录音
async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];
        
        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };
        
        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            await handleAudioRecorded(audioBlob);
            
            // 停止所有音轨
            stream.getTracks().forEach(track => track.stop());
        };
        
        mediaRecorder.start();
        isRecording = true;
        
        // 更新 UI
        recordBtn.classList.add('recording');
        recordBtn.querySelector('.text').textContent = '点击停止录音';
        recordingStatus.classList.remove('hidden');
        
    } catch (error) {
        console.error('录音失败:', error);
        showError('无法访问麦克风，请检查权限设置');
    }
}

// 停止录音
function stopRecording() {
    if (mediaRecorder && isRecording) {
        mediaRecorder.stop();
        isRecording = false;
        
        // 更新 UI
        recordBtn.classList.remove('recording');
        recordBtn.querySelector('.text').textContent = '点击开始录音';
        recordingStatus.classList.add('hidden');
    }
}

// 处理录音完成
async function handleAudioRecorded(audioBlob) {
    showLoading('正在识别语音...');
    
    try {
        // 转换为 base64
        const audioBase64 = await blobToBase64(audioBlob);
        
        // 提交导航请求
        await submitNavigate({
            type: 'audio',
            audio: audioBase64,
            format: 'webm'
        });
        
    } catch (error) {
        console.error('处理录音失败:', error);
        showError('处理录音失败: ' + error.message);
    }
}

// Blob 转 Base64
function blobToBase64(blob) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onloadend = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsDataURL(blob);
    });
}

// 初始化提交
function initSubmit() {
    submitBtn.addEventListener('click', handleSubmit);
    
    // 支持回车提交
    textInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
            handleSubmit();
        }
    });
}

// 处理提交
async function handleSubmit() {
    if (currentInputType === 'text') {
        const text = textInput.value.trim();
        if (!text) {
            showError('请输入导航信息');
            return;
        }
        
        await submitNavigate({
            type: 'text',
            input: text
        });
    } else {
        showError('请点击麦克风按钮开始录音');
    }
}

// 提交导航请求
async function submitNavigate(baseData) {
    showLoading('AI 正在处理...');
    
    try {
        const requestData = {
            ...baseData,
            ai_provider: aiProviderSelect.value || undefined,
            map_provider: mapProviderSelect.value || undefined
        };
        
        const response = await fetch('/api/navigate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            showSuccess(data);
            
            // 跳转到地图
            setTimeout(() => {
                window.location.href = data.url;
            }, 2000);
        } else {
            showError(data.error || '未知错误', data.error_type);
        }
        
    } catch (error) {
        console.error('请求失败:', error);
        showError('网络请求失败: ' + error.message);
    } finally {
        hideLoading();
    }
}

// 显示加载状态
function showLoading(message = '处理中...') {
    loadingText.textContent = message;
    loadingSection.classList.remove('hidden');
    resultSection.classList.add('hidden');
    submitBtn.disabled = true;
}

// 隐藏加载状态
function hideLoading() {
    loadingSection.classList.add('hidden');
    submitBtn.disabled = false;
}

// 显示成功结果
function showSuccess(data) {
    const html = `
        <div class="result-success">
            <h4>✅ 导航成功！</h4>
            ${data.recognized_text ? `<p class="result-info"><strong>识别文本：</strong>${data.recognized_text}</p>` : ''}
            <p class="result-info"><strong>起点：</strong>${data.start || '(未指定)'}</p>
            <p class="result-info"><strong>终点：</strong>${data.end}</p>
            <p class="result-info"><strong>地图：</strong>${getMapName(data.map_provider)}</p>
            ${data.stt_provider ? `<p class="result-info"><strong>语音识别：</strong>${data.stt_provider}</p>` : ''}
            <p class="result-info"><strong>AI 模型：</strong>${data.ai_provider}</p>
            <p class="result-info"><strong>导航 URL：</strong><a href="${data.url}" target="_blank">点击打开</a></p>
            <p style="margin-top: 15px; color: #28a745;">
                🚀 2秒后自动跳转到地图...
            </p>
        </div>
    `;
    
    resultContent.innerHTML = html;
    resultSection.classList.remove('hidden');
}

// 显示错误
function showError(message, errorType = 'unknown') {
    const html = `
        <div class="result-error">
            <h4>❌ 错误</h4>
            <p class="result-info"><strong>错误类型：</strong>${getErrorTypeName(errorType)}</p>
            <p class="result-info"><strong>详情：</strong>${message}</p>
            <p style="margin-top: 15px; color: #dc3545;">
                💡 请检查输入并重试
            </p>
        </div>
    `;
    
    resultContent.innerHTML = html;
    resultSection.classList.remove('hidden');
}

// 获取地图名称
function getMapName(provider) {
    const names = {
        'baidu': '百度地图',
        'amap': '高德地图',
        'google': 'Google Maps'
    };
    return names[provider] || provider;
}

// 获取错误类型名称
function getErrorTypeName(errorType) {
    const names = {
        'invalid_request': '无效请求',
        'stt_failed': '语音识别失败',
        'ai_not_available': 'AI 服务不可用',
        'extraction_failed': '提取导航信息失败',
        'no_location': '未识别到地点',
        'map_generation_failed': '生成地图链接失败',
        'unknown': '未知错误'
    };
    return names[errorType] || errorType;
}
