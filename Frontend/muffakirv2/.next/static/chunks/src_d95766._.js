(globalThis.TURBOPACK = globalThis.TURBOPACK || []).push(["static/chunks/src_d95766._.js", {

"[project]/src/components/ThemeToggle.tsx [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { r: __turbopack_require__, f: __turbopack_module_context__, i: __turbopack_import__, s: __turbopack_esm__, v: __turbopack_export_value__, n: __turbopack_export_namespace__, c: __turbopack_cache__, M: __turbopack_modules__, l: __turbopack_load__, j: __turbopack_dynamic__, P: __turbopack_resolve_absolute_path__, U: __turbopack_relative_url__, R: __turbopack_resolve_module_id_path__, b: __turbopack_worker_blob_url__, g: global, __dirname, k: __turbopack_refresh__, m: module, z: __turbopack_require_stub__ } = __turbopack_context__;
{
__turbopack_esm__({
    "default": (()=>__TURBOPACK__default__export__)
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_import__("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_import__("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$react$2d$icons$2f$fa$2f$index$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_import__("[project]/node_modules/react-icons/fa/index.mjs [app-client] (ecmascript)");
;
var _s = __turbopack_refresh__.signature();
'use client';
;
;
function ThemeToggle() {
    _s();
    const [darkMode, setDarkMode] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])({
        "ThemeToggle.useState": ()=>{
            if ("TURBOPACK compile-time truthy", 1) {
                return localStorage.getItem('theme') === 'dark';
            }
            "TURBOPACK unreachable";
        }
    }["ThemeToggle.useState"]);
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "ThemeToggle.useEffect": ()=>{
            const savedTheme = localStorage.getItem('theme');
            setDarkMode(savedTheme === 'dark');
        }
    }["ThemeToggle.useEffect"], []);
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "ThemeToggle.useEffect": ()=>{
            if (darkMode) {
                document.documentElement.setAttribute('theme', 'dark');
                localStorage.setItem('theme', 'dark');
            } else {
                document.documentElement.setAttribute('theme', 'light');
                localStorage.setItem('theme', 'light');
            }
        }
    }["ThemeToggle.useEffect"], [
        darkMode
    ]);
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
        className: "theme-toggle",
        onClick: ()=>setDarkMode(!darkMode),
        "aria-label": darkMode ? 'Switch to light mode' : 'Switch to dark mode',
        children: darkMode ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$react$2d$icons$2f$fa$2f$index$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__["FaSun"], {
            size: 20
        }, void 0, false, {
            fileName: "[project]/src/components/ThemeToggle.tsx",
            lineNumber: 37,
            columnNumber: 19
        }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$react$2d$icons$2f$fa$2f$index$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__["FaMoon"], {
            size: 20
        }, void 0, false, {
            fileName: "[project]/src/components/ThemeToggle.tsx",
            lineNumber: 37,
            columnNumber: 41
        }, this)
    }, void 0, false, {
        fileName: "[project]/src/components/ThemeToggle.tsx",
        lineNumber: 32,
        columnNumber: 5
    }, this);
}
_s(ThemeToggle, "MVbVjpZ+Lc2PGXHUn8fPkTZinwU=");
_c = ThemeToggle;
const __TURBOPACK__default__export__ = ThemeToggle;
var _c;
__turbopack_refresh__.register(_c, "ThemeToggle");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_refresh__.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
"[project]/src/components/LanguageToggle.tsx [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { r: __turbopack_require__, f: __turbopack_module_context__, i: __turbopack_import__, s: __turbopack_esm__, v: __turbopack_export_value__, n: __turbopack_export_namespace__, c: __turbopack_cache__, M: __turbopack_modules__, l: __turbopack_load__, j: __turbopack_dynamic__, P: __turbopack_resolve_absolute_path__, U: __turbopack_relative_url__, R: __turbopack_resolve_module_id_path__, b: __turbopack_worker_blob_url__, g: global, __dirname, k: __turbopack_refresh__, m: module, z: __turbopack_require_stub__ } = __turbopack_context__;
{
__turbopack_esm__({
    "default": (()=>__TURBOPACK__default__export__)
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_import__("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$react$2d$icons$2f$fa$2f$index$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_import__("[project]/node_modules/react-icons/fa/index.mjs [app-client] (ecmascript)");
'use client';
;
;
function LanguageToggle({ lang, onToggle }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
        className: "language-toggle",
        onClick: onToggle,
        "aria-label": "Toggle language",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$react$2d$icons$2f$fa$2f$index$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__["FaGlobe"], {
                size: 20
            }, void 0, false, {
                fileName: "[project]/src/components/LanguageToggle.tsx",
                lineNumber: 13,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                children: lang === 'en' ? 'AR' : 'EN'
            }, void 0, false, {
                fileName: "[project]/src/components/LanguageToggle.tsx",
                lineNumber: 14,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/src/components/LanguageToggle.tsx",
        lineNumber: 8,
        columnNumber: 5
    }, this);
}
_c = LanguageToggle;
const __TURBOPACK__default__export__ = LanguageToggle;
var _c;
__turbopack_refresh__.register(_c, "LanguageToggle");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_refresh__.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
"[project]/src/translations/translations.ts [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { r: __turbopack_require__, f: __turbopack_module_context__, i: __turbopack_import__, s: __turbopack_esm__, v: __turbopack_export_value__, n: __turbopack_export_namespace__, c: __turbopack_cache__, M: __turbopack_modules__, l: __turbopack_load__, j: __turbopack_dynamic__, P: __turbopack_resolve_absolute_path__, U: __turbopack_relative_url__, R: __turbopack_resolve_module_id_path__, b: __turbopack_worker_blob_url__, g: global, __dirname, k: __turbopack_refresh__, m: module, z: __turbopack_require_stub__ } = __turbopack_context__;
{
__turbopack_esm__({
    "default": (()=>__TURBOPACK__default__export__)
});
const translations = {
    en: {
        welcome: "Welcome to Muffakir",
        useNow: "Use Muffakir Now",
        signIn: "Sign In",
        typeMessage: "Type your message here...",
        search: "Search",
        documents: "Documents",
        test: "Test Yourself",
        testTitle: "Knowledge Test",
        question: "Question",
        of: "of",
        previous: "Previous",
        next: "Next",
        submit: "Submit Test",
        yourScore: "Your Score:",
        tryAgain: "Try Again",
        question1: "What is the capital of France?",
        option1a: "Paris",
        option1b: "London",
        option1c: "Berlin",
        option1d: "Madrid",
        question2: "What is the largest planet in our Solar System?",
        option2a: "Jupiter",
        option2b: "Saturn",
        option2c: "Earth",
        option2d: "Mars",
        guest: "Guest"
    },
    ar: {
        welcome: "مرحبا بكم في مفكر",
        useNow: "استخدم مفكر الآن",
        signIn: "تسجيل الدخول",
        typeMessage: "اكتب رسالتك هنا...",
        search: "بحث",
        documents: "المستندات",
        test: "اختبر نفسك",
        testTitle: "اختبار المعرفة",
        question: "السؤال",
        of: "من",
        previous: "السابق",
        next: "التالي",
        submit: "تقديم الإجابات",
        yourScore: "نتيجتك:",
        tryAgain: "إعادة المحاولة",
        question1: "ما هي عاصمة فرنسا؟",
        option1a: "باريس",
        option1b: "لندن",
        option1c: "برلين",
        option1d: "مدريد",
        question2: "ما هو أكبر كوكب في المجموعة الشمسية؟",
        option2a: "المشتري",
        option2b: "زحل",
        option2c: "الأرض",
        option2d: "المريخ",
        guest: "زائر"
    }
};
const __TURBOPACK__default__export__ = translations;
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_refresh__.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
"[project]/src/components/UserProfile.tsx [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { r: __turbopack_require__, f: __turbopack_module_context__, i: __turbopack_import__, s: __turbopack_esm__, v: __turbopack_export_value__, n: __turbopack_export_namespace__, c: __turbopack_cache__, M: __turbopack_modules__, l: __turbopack_load__, j: __turbopack_dynamic__, P: __turbopack_resolve_absolute_path__, U: __turbopack_relative_url__, R: __turbopack_resolve_module_id_path__, b: __turbopack_worker_blob_url__, g: global, __dirname, k: __turbopack_refresh__, m: module, z: __turbopack_require_stub__ } = __turbopack_context__;
{
__turbopack_esm__({
    "default": (()=>__TURBOPACK__default__export__)
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_import__("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$react$2d$icons$2f$pi$2f$index$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_import__("[project]/node_modules/react-icons/pi/index.mjs [app-client] (ecmascript)");
;
;
const UserProfile = ({ guest })=>{
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "profile",
        children: [
            guest,
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$react$2d$icons$2f$pi$2f$index$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__["PiStudentBold"], {
                size: 32
            }, void 0, false, {
                fileName: "[project]/src/components/UserProfile.tsx",
                lineNumber: 9,
                columnNumber: 9
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/src/components/UserProfile.tsx",
        lineNumber: 7,
        columnNumber: 5
    }, this);
};
_c = UserProfile;
const __TURBOPACK__default__export__ = UserProfile;
var _c;
__turbopack_refresh__.register(_c, "UserProfile");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_refresh__.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
"[project]/src/components/Test.tsx [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { r: __turbopack_require__, f: __turbopack_module_context__, i: __turbopack_import__, s: __turbopack_esm__, v: __turbopack_export_value__, n: __turbopack_export_namespace__, c: __turbopack_cache__, M: __turbopack_modules__, l: __turbopack_load__, j: __turbopack_dynamic__, P: __turbopack_resolve_absolute_path__, U: __turbopack_relative_url__, R: __turbopack_resolve_module_id_path__, b: __turbopack_worker_blob_url__, g: global, __dirname, k: __turbopack_refresh__, m: module, z: __turbopack_require_stub__ } = __turbopack_context__;
{
__turbopack_esm__({
    "default": (()=>__TURBOPACK__default__export__)
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_import__("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_import__("[project]/node_modules/next/dist/client/app-dir/link.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$ThemeToggle$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_import__("[project]/src/components/ThemeToggle.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$LanguageToggle$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_import__("[project]/src/components/LanguageToggle.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$translations$2f$translations$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_import__("[project]/src/translations/translations.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_import__("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$UserProfile$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_import__("[project]/src/components/UserProfile.tsx [app-client] (ecmascript)");
;
var _s = __turbopack_refresh__.signature();
'use client';
;
;
;
;
;
;
function TestPage() {
    _s();
    const [lang, setLang] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])('en');
    const [currentQuestion, setCurrentQuestion] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(0);
    const [userAnswers, setUserAnswers] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])([]);
    const [score, setScore] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(null);
    // Sample questions - replace with your actual questions
    const questions = [
        {
            id: 1,
            text: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$translations$2f$translations$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"][lang].question1,
            options: [
                __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$translations$2f$translations$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"][lang].option1a,
                __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$translations$2f$translations$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"][lang].option1b,
                __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$translations$2f$translations$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"][lang].option1c,
                __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$translations$2f$translations$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"][lang].option1d
            ],
            correctAnswer: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$translations$2f$translations$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"][lang].option1a
        },
        {
            id: 2,
            text: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$translations$2f$translations$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"][lang].question2,
            options: [
                __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$translations$2f$translations$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"][lang].option2a,
                __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$translations$2f$translations$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"][lang].option2b,
                __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$translations$2f$translations$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"][lang].option2c,
                __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$translations$2f$translations$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"][lang].option2d
            ],
            correctAnswer: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$translations$2f$translations$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"][lang].option2a
        }
    ];
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "TestPage.useEffect": ()=>{
            const savedLang = localStorage.getItem('lang') === 'ar' ? 'ar' : 'en';
            setLang(savedLang);
            document.documentElement.setAttribute('lang', savedLang);
        }
    }["TestPage.useEffect"], []);
    const handleLanguageChange = ()=>{
        const newLang = lang === 'en' ? 'ar' : 'en';
        setLang(newLang);
        localStorage.setItem('lang', newLang);
        document.documentElement.setAttribute('lang', newLang);
    };
    const handleAnswerSelect = (answer)=>{
        const newAnswers = [
            ...userAnswers
        ];
        newAnswers[currentQuestion] = answer;
        setUserAnswers(newAnswers);
    };
    const handleNextQuestion = ()=>{
        if (currentQuestion < questions.length - 1) {
            setCurrentQuestion((prev)=>prev + 1);
        }
    };
    const handlePreviousQuestion = ()=>{
        if (currentQuestion > 0) {
            setCurrentQuestion((prev)=>prev - 1);
        }
    };
    const calculateScore = ()=>{
        const correct = questions.filter((q, index)=>userAnswers[index] === q.correctAnswer).length;
        setScore(correct);
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("main", {
        className: "container",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$ThemeToggle$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {}, void 0, false, {
                fileName: "[project]/src/components/Test.tsx",
                lineNumber: 92,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$LanguageToggle$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
                lang: lang,
                onToggle: handleLanguageChange
            }, void 0, false, {
                fileName: "[project]/src/components/Test.tsx",
                lineNumber: 93,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$UserProfile$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
                guest: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$translations$2f$translations$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"][lang].guest
            }, void 0, false, {
                fileName: "[project]/src/components/Test.tsx",
                lineNumber: 94,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "test-container",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
                        href: "/",
                        className: "title-link",
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h1", {
                            className: "title",
                            children: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$translations$2f$translations$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"][lang].testTitle
                        }, void 0, false, {
                            fileName: "[project]/src/components/Test.tsx",
                            lineNumber: 98,
                            columnNumber: 11
                        }, this)
                    }, void 0, false, {
                        fileName: "[project]/src/components/Test.tsx",
                        lineNumber: 97,
                        columnNumber: 9
                    }, this),
                    score === null ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "question-container",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "progress",
                                children: [
                                    __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$translations$2f$translations$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"][lang].question,
                                    " ",
                                    currentQuestion + 1,
                                    " ",
                                    __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$translations$2f$translations$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"][lang].of,
                                    " ",
                                    questions.length
                                ]
                            }, void 0, true, {
                                fileName: "[project]/src/components/Test.tsx",
                                lineNumber: 103,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "question-card",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                                        children: questions[currentQuestion].text
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/Test.tsx",
                                        lineNumber: 108,
                                        columnNumber: 15
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "options-container",
                                        children: questions[currentQuestion].options.map((option, index)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                                className: `option-button ${userAnswers[currentQuestion] === option ? 'selected' : ''}`,
                                                onClick: ()=>handleAnswerSelect(option),
                                                children: option
                                            }, index, false, {
                                                fileName: "[project]/src/components/Test.tsx",
                                                lineNumber: 111,
                                                columnNumber: 19
                                            }, this))
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/Test.tsx",
                                        lineNumber: 109,
                                        columnNumber: 15
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/src/components/Test.tsx",
                                lineNumber: 107,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "navigation-buttons",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        className: "nav-button prev-button",
                                        onClick: handlePreviousQuestion,
                                        disabled: currentQuestion === 0,
                                        children: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$translations$2f$translations$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"][lang].previous
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/Test.tsx",
                                        lineNumber: 125,
                                        columnNumber: 15
                                    }, this),
                                    currentQuestion < questions.length - 1 ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        className: "nav-button next-button",
                                        onClick: handleNextQuestion,
                                        children: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$translations$2f$translations$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"][lang].next
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/Test.tsx",
                                        lineNumber: 134,
                                        columnNumber: 17
                                    }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        className: "nav-button submit-button",
                                        onClick: calculateScore,
                                        children: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$translations$2f$translations$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"][lang].submit
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/Test.tsx",
                                        lineNumber: 141,
                                        columnNumber: 17
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/src/components/Test.tsx",
                                lineNumber: 124,
                                columnNumber: 13
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/components/Test.tsx",
                        lineNumber: 102,
                        columnNumber: 11
                    }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "result-container",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                                children: [
                                    __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$translations$2f$translations$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"][lang].yourScore,
                                    " ",
                                    score,
                                    "/",
                                    questions.length
                                ]
                            }, void 0, true, {
                                fileName: "[project]/src/components/Test.tsx",
                                lineNumber: 152,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                className: "restart-button",
                                onClick: ()=>{
                                    setCurrentQuestion(0);
                                    setUserAnswers([]);
                                    setScore(null);
                                },
                                children: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$translations$2f$translations$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"][lang].tryAgain
                            }, void 0, false, {
                                fileName: "[project]/src/components/Test.tsx",
                                lineNumber: 153,
                                columnNumber: 13
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/components/Test.tsx",
                        lineNumber: 151,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/src/components/Test.tsx",
                lineNumber: 96,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/src/components/Test.tsx",
        lineNumber: 91,
        columnNumber: 5
    }, this);
}
_s(TestPage, "7X9/bj08IMkgmI+bJVUPBGz+Yu0=");
_c = TestPage;
const __TURBOPACK__default__export__ = TestPage;
var _c;
__turbopack_refresh__.register(_c, "TestPage");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_refresh__.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
"[project]/src/app/test/page.tsx [app-rsc] (ecmascript, Next.js server component, client modules)": ((__turbopack_context__) => {

var { r: __turbopack_require__, f: __turbopack_module_context__, i: __turbopack_import__, s: __turbopack_esm__, v: __turbopack_export_value__, n: __turbopack_export_namespace__, c: __turbopack_cache__, M: __turbopack_modules__, l: __turbopack_load__, j: __turbopack_dynamic__, P: __turbopack_resolve_absolute_path__, U: __turbopack_relative_url__, R: __turbopack_resolve_module_id_path__, b: __turbopack_worker_blob_url__, g: global, __dirname, t: __turbopack_require_real__ } = __turbopack_context__;
{
}}),
}]);

//# sourceMappingURL=src_d95766._.js.map