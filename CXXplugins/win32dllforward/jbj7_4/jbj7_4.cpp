﻿// jbj7.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//
#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include<Windows.h>
#include <io.h>
#include <fcntl.h>

#define CODEPAGE_JA  932
#define CODEPAGE_GB  936 

#define CODEPAGE_BIG5 950

#pragma comment( linker, "/subsystem:windows /entry:wmainCRTStartup" )
UINT unpackuint32(unsigned char* s) {
    int i = 0;
    return ((s[i]) << 24) | ((s[i + 1]) << 16) | ((s[i + 2]) << 8) | (s[i + 3]) ;
}
void packuint32(UINT i, unsigned char* b) {
    b[0] = (i >> 24) & 0xff;
    b[1] = (i >> 16) & 0xff;
    b[2] = (i >> 8) & 0xff;
    b[3] = (i) & 0xff; 
}
void readlen(HANDLE hPipe, int l, unsigned char* cache) {
    DWORD  _; DWORD readen = 0;
    while (readen < l) {
        ReadFile(hPipe, cache+readen, l-readen, &_, NULL);
        readen += _;
    }
    
}
void writelen(HANDLE hPipe, int l, unsigned char* cache) {
    DWORD  _; DWORD readen = 0;
    while (readen < l) {
        WriteFile(hPipe, cache + readen, l - readen, &_, NULL);
        readen += _; 
    }

}

static UINT64 getCurrentMilliSecTimestamp() {
    FILETIME file_time;
    GetSystemTimeAsFileTime(&file_time);
    UINT64 time = ((UINT64)file_time.dwLowDateTime) + ((UINT64)file_time.dwHighDateTime << 32);

    // This magic number is the number of 100 nanosecond intervals since January 1, 1601 (UTC)
    // until 00:00:00 January 1, 1970
    static const UINT64 EPOCH = ((UINT64)116444736000000000ULL);

    return (UINT64)((time - EPOCH) / 10000LL);
}
int wmain(int argc, wchar_t* argv[])
{
    HANDLE hPipe = CreateNamedPipe(argv[2], PIPE_ACCESS_DUPLEX, PIPE_TYPE_MESSAGE | PIPE_READMODE_MESSAGE | PIPE_WAIT
        , PIPE_UNLIMITED_INSTANCES, 65535, 65535, NMPWAIT_WAIT_FOREVER, 0);

    /*_setmode(_fileno(stdout), _O_U16TEXT);
    _setmode(_fileno(stdin), _O_U16TEXT);*/
    fclose(stdout);

    //system("chcp 932");
    HMODULE module = LoadLibraryW(argv[1]);
    typedef int(*_JC_Transfer_Unicode)(int, UINT, UINT, int, int, LPCWSTR, LPWSTR, int&, LPWSTR, int&);
    typedef int(__cdecl* _DJC_OpenAllUserDic_Unicode)(LPWSTR, int unknown);
    auto JC_Transfer_Unicode = (_JC_Transfer_Unicode)GetProcAddress(module, "JC_Transfer_Unicode");
    auto DJC_OpenAllUserDic_Unicode = (_DJC_OpenAllUserDic_Unicode)GetProcAddress(module, "DJC_OpenAllUserDic_Unicode");


    int USERDIC_PATH_SIZE = 0x204;
    int MAX_USERDIC_COUNT = 3;
    int USERDIC_BUFFER_SIZE = USERDIC_PATH_SIZE * MAX_USERDIC_COUNT;// 1548, sizeof(wchar_t)
    wchar_t cache[1548] = { 0 };
    for (int i = 4; i < argc; i++) {
        wcscpy(cache + (i - 4) * USERDIC_PATH_SIZE, argv[i]);
    }
    DJC_OpenAllUserDic_Unicode(cache, 0);
    wchar_t *fr = new wchar_t[3000];
    wchar_t* to= new wchar_t[3000];
    wchar_t *buf = new wchar_t[3000];
    SECURITY_DESCRIPTOR sd = {};
    InitializeSecurityDescriptor(&sd, SECURITY_DESCRIPTOR_REVISION);
    SetSecurityDescriptorDacl(&sd, TRUE, NULL, FALSE);
    SECURITY_ATTRIBUTES allAccess = SECURITY_ATTRIBUTES{ sizeof(SECURITY_ATTRIBUTES), &sd, FALSE };
    SetEvent(CreateEvent(&allAccess, FALSE, FALSE, argv[3]));
    if (ConnectNamedPipe(hPipe, NULL) != NULL) {
        DWORD len = 0;

    }
    unsigned char intcache[4];
    while (true) {
        memset(fr, 0, 3000 * sizeof(wchar_t));
        memset(to, 0, 3000 * sizeof(wchar_t));
        memset(buf, 0, 3000 * sizeof(wchar_t)); 
        int a = 3000;
        int b = 3000; 
        char codec[4] = { 0 };
        UINT code;
        DWORD _;
        UINT datalen;
        readlen(hPipe, 4, intcache); 
        code = unpackuint32(intcache);
        readlen(hPipe, 4, intcache);
        datalen = unpackuint32(intcache);
        readlen(hPipe, datalen, (unsigned char*)fr);
        //std::wcout << getCurrentMilliSecTimestamp() << std::endl;
        JC_Transfer_Unicode(0, CODEPAGE_JA, code, 1, 1, fr, to, a, buf, b);
        //std::wcout << getCurrentMilliSecTimestamp() << std::endl;
        datalen = 2 * wcslen(to);
        packuint32(datalen, intcache);  
        writelen(hPipe, 4, intcache); 
        writelen(hPipe, datalen,(unsigned char*) to);  
    }

}
// 运行程序: Ctrl + F5 或调试 >“开始执行(不调试)”菜单
// 调试程序: F5 或调试 >“开始调试”菜单

// 入门使用技巧: 
//   1. 使用解决方案资源管理器窗口添加/管理文件
//   2. 使用团队资源管理器窗口连接到源代码管理
//   3. 使用输出窗口查看生成输出和其他消息
//   4. 使用错误列表窗口查看错误
//   5. 转到“项目”>“添加新项”以创建新的代码文件，或转到“项目”>“添加现有项”以将现有代码文件添加到项目
//   6. 将来，若要再次打开此项目，请转到“文件”>“打开”>“项目”并选择 .sln 文件
