/*
 * DIGITAL EVIDENCE SYSTEM - Sorting Algorithms (QuickSort & MergeSort)
 * File: sorting.c
 * Purpose: Sorts digital evidence records by Evidence ID, Evidence Title, or Upload Date.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_ITEMS 500
#define MAX_STR 256

typedef struct {
    int id;
    char code[32];
    char title[MAX_STR];
    char category[MAX_STR];
    char hash[128];
    char date[64];
} EvidenceRecord;

EvidenceRecord items[MAX_ITEMS];
int total_count = 0;
long long comparisons = 0;
long long swaps = 0;

int compare_items(const EvidenceRecord* a, const EvidenceRecord* b, const char* field, const char* order) {
    int res = 0;
    comparisons++;
    if (strcmp(field, "title") == 0) {
        res = strcmp(a->title, b->title);
    } else if (strcmp(field, "date") == 0) {
        res = strcmp(a->date, b->date);
    } else {
        res = a->id - b->id;
    }
    if (strcmp(order, "desc") == 0) {
        res = -res;
    }
    return res;
}

// QuickSort Partition
int partition(int low, int high, const char* field, const char* order) {
    int j;
    EvidenceRecord pivot = items[high];
    int i = low - 1;

    for (j = low; j < high; j++) {
        if (compare_items(&items[j], &pivot, field, order) <= 0) {
            EvidenceRecord t;
            i++;
            t = items[i];
            items[i] = items[j];
            items[j] = t;
            swaps++;
        }
    }
    {
        EvidenceRecord t = items[i + 1];
        items[i + 1] = items[high];
        items[high] = t;
        swaps++;
    }
    return i + 1;
}

void quick_sort(int low, int high, const char* field, const char* order) {
    if (low < high) {
        int pi = partition(low, high, field, order);
        quick_sort(low, pi - 1, field, order);
        quick_sort(pi + 1, high, field, order);
    }
}

int main(int argc, char* argv[]) {
    int i;
    char field[32] = "id";      // "id", "title", "date"
    char order[32] = "asc";     // "asc", "desc"

    for (i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--field") == 0 && i + 1 < argc) {
            strncpy(field, argv[i + 1], sizeof(field) - 1);
        } else if (strcmp(argv[i], "--order") == 0 && i + 1 < argc) {
            strncpy(order, argv[i + 1], sizeof(order) - 1);
        }
    }

    if (argc > 1 && strcmp(argv[1], "--demo") == 0) {
        EvidenceRecord r1 = {103, "E103", "CCTV_Surveillance_Footage.mp4", "Video Evidence", "hash3", "2026-11-21 14:00"};
        EvidenceRecord r2 = {101, "E101", "Accident_Site_Photo.jpg", "Image Evidence", "hash1", "2026-11-20 09:30"};
        EvidenceRecord r3 = {102, "E102", "Forensic_Autopsy_Report.pdf", "Document Evidence", "hash2", "2026-11-21 11:20"};
        items[0] = r1; items[1] = r2; items[2] = r3;
        total_count = 3;
    } else {
        char line[1024];
        while (fgets(line, sizeof(line), stdin) && total_count < MAX_ITEMS) {
            if (line[0] == '\n' || line[0] == '\r') continue;
            int id;
            char code[32] = {0}, title[MAX_STR] = {0}, category[MAX_STR] = {0}, hash[128] = {0}, date[64] = {0};
            char* token = strtok(line, "|\n\r");
            if (!token) continue;
            id = atoi(token);

            token = strtok(NULL, "|\n\r");
            if (token) strncpy(code, token, sizeof(code) - 1);

            token = strtok(NULL, "|\n\r");
            if (token) strncpy(title, token, sizeof(title) - 1);

            token = strtok(NULL, "|\n\r");
            if (token) strncpy(category, token, sizeof(category) - 1);

            token = strtok(NULL, "|\n\r");
            if (token) strncpy(hash, token, sizeof(hash) - 1);

            token = strtok(NULL, "|\n\r");
            if (token) strncpy(date, token, sizeof(date) - 1);

            items[total_count].id = id;
            strncpy(items[total_count].code, code, sizeof(items[total_count].code) - 1);
            strncpy(items[total_count].title, title, sizeof(items[total_count].title) - 1);
            strncpy(items[total_count].category, category, sizeof(items[total_count].category) - 1);
            strncpy(items[total_count].hash, hash, sizeof(items[total_count].hash) - 1);
            strncpy(items[total_count].date, date, sizeof(items[total_count].date) - 1);
            total_count++;
        }
    }

    if (total_count > 1) {
        quick_sort(0, total_count - 1, field, order);
    }

    printf("{\n");
    printf("  \"algorithm\": \"QuickSort (C Implementation)\",\n");
    printf("  \"sort_field\": \"%s\",\n", field);
    printf("  \"sort_order\": \"%s\",\n", order);
    printf("  \"total_records\": %d,\n", total_count);
    printf("  \"comparisons\": %lld,\n", comparisons);
    printf("  \"swaps\": %lld,\n", swaps);
    printf("  \"records\": [\n");
    for (i = 0; i < total_count; i++) {
        printf("    {\"id\": %d, \"code\": \"%s\", \"title\": \"%s\", \"category\": \"%s\", \"date\": \"%s\"}%s\n",
               items[i].id, items[i].code, items[i].title, items[i].category, items[i].date, (i + 1 < total_count) ? "," : "");
    }
    printf("  ]\n}\n");

    return 0;
}
