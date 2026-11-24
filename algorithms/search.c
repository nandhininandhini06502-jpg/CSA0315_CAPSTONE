/*
 * DIGITAL EVIDENCE SYSTEM - Search Algorithms
 * File: search.c
 * Purpose: Binary Search (on sorted ID array) and Linear Search (on titles/keywords).
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

int binary_search(int target_id, int* steps) {
    int low = 0, high = total_count - 1;
    *steps = 0;
    while (low <= high) {
        int mid;
        (*steps)++;
        mid = low + (high - low) / 2;
        if (items[mid].id == target_id) return mid;
        if (items[mid].id < target_id) low = mid + 1;
        else high = mid - 1;
    }
    return -1;
}

int linear_search_title(const char* query, int* steps) {
    int i;
    *steps = 0;
    for (i = 0; i < total_count; i++) {
        (*steps)++;
        if (strstr(items[i].title, query) != NULL || strstr(items[i].code, query) != NULL) {
            return i;
        }
    }
    return -1;
}

int main(int argc, char* argv[]) {
    int i;
    int steps = 0;
    int found_index = -1;
    char search_type[32] = "binary"; // "binary" or "linear"
    char query[128] = "";

    for (i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--type") == 0 && i + 1 < argc) {
            strncpy(search_type, argv[i + 1], sizeof(search_type) - 1);
        } else if (strcmp(argv[i], "--query") == 0 && i + 1 < argc) {
            strncpy(query, argv[i + 1], sizeof(query) - 1);
        }
    }

    if (argc > 1 && strcmp(argv[1], "--demo") == 0) {
        EvidenceRecord r1 = {101, "E101", "Accident_Site_Photo.jpg", "Image Evidence", "hash1", "2026-11-20"};
        EvidenceRecord r2 = {102, "E102", "Forensic_Autopsy_Report.pdf", "Document Evidence", "hash2", "2026-11-21"};
        EvidenceRecord r3 = {103, "E103", "CCTV_Surveillance_Footage.mp4", "Video Evidence", "hash3", "2026-11-21"};
        items[0] = r1; items[1] = r2; items[2] = r3;
        total_count = 3;
        strcpy(query, "102");
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

    if (strcmp(search_type, "binary") == 0) {
        int target_id = atoi(query);
        found_index = binary_search(target_id, &steps);
    } else {
        found_index = linear_search_title(query, &steps);
    }

    printf("{\n");
    printf("  \"algorithm\": \"%s\",\n", strcmp(search_type, "binary") == 0 ? "Binary Search (O(log n))" : "Linear Search (O(n))");
    printf("  \"query\": \"%s\",\n", query);
    printf("  \"comparisons\": %d,\n", steps);
    printf("  \"found\": %s,\n", (found_index != -1) ? "true" : "false");
    if (found_index != -1) {
        printf("  \"item\": {\n");
        printf("    \"id\": %d,\n", items[found_index].id);
        printf("    \"code\": \"%s\",\n", items[found_index].code);
        printf("    \"title\": \"%s\",\n", items[found_index].title);
        printf("    \"category\": \"%s\"\n", items[found_index].category);
        printf("  }\n");
    } else {
        printf("  \"item\": null\n");
    }
    printf("}\n");

    return 0;
}
