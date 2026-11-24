/*
 * DIGITAL EVIDENCE SYSTEM - Hash Table Algorithm
 * File: hashtable.c
 * Purpose: Fast O(1) average lookup of digital evidence using a hash table with separate chaining.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TABLE_SIZE 31
#define MAX_STR 256

typedef struct HashNode {
    int id;
    char code[32];
    char title[MAX_STR];
    char category[MAX_STR];
    char hash[128];
    char date[64];
    struct HashNode* next;
} HashNode;

typedef struct {
    HashNode* buckets[TABLE_SIZE];
    int total_entries;
    int collisions;
} HashTable;

HashTable* create_table() {
    int i;
    HashTable* table = (HashTable*)malloc(sizeof(HashTable));
    for (i = 0; i < TABLE_SIZE; i++) {
        table->buckets[i] = NULL;
    }
    table->total_entries = 0;
    table->collisions = 0;
    return table;
}

unsigned int hash_code(const char* str) {
    unsigned int hash = 5381;
    int c;
    while ((c = *str++)) {
        hash = ((hash << 5) + hash) + c; /* hash * 33 + c */
    }
    return hash % TABLE_SIZE;
}

void hash_insert(HashTable* table, int id, const char* code, const char* title, const char* category, const char* hash, const char* date) {
    unsigned int index = hash_code(code);
    HashNode* new_node = (HashNode*)malloc(sizeof(HashNode));
    new_node->id = id;
    strncpy(new_node->code, code, sizeof(new_node->code) - 1);
    new_node->code[sizeof(new_node->code) - 1] = '\0';
    strncpy(new_node->title, title, sizeof(new_node->title) - 1);
    new_node->title[sizeof(new_node->title) - 1] = '\0';
    strncpy(new_node->category, category, sizeof(new_node->category) - 1);
    new_node->category[sizeof(new_node->category) - 1] = '\0';
    strncpy(new_node->hash, hash, sizeof(new_node->hash) - 1);
    new_node->hash[sizeof(new_node->hash) - 1] = '\0';
    strncpy(new_node->date, date, sizeof(new_node->date) - 1);
    new_node->date[sizeof(new_node->date) - 1] = '\0';
    new_node->next = NULL;

    if (table->buckets[index] == NULL) {
        table->buckets[index] = new_node;
    } else {
        table->collisions++;
        new_node->next = table->buckets[index];
        table->buckets[index] = new_node;
    }
    table->total_entries++;
}

HashNode* hash_search(HashTable* table, const char* code, int* out_bucket, int* out_comparisons) {
    unsigned int index = hash_code(code);
    *out_bucket = index;
    int comps = 0;
    HashNode* curr = table->buckets[index];
    while (curr) {
        comps++;
        if (strcmp(curr->code, code) == 0) {
            *out_comparisons = comps;
            return curr;
        }
        curr = curr->next;
    }
    *out_comparisons = comps;
    return NULL;
}

int main(int argc, char* argv[]) {
    int i;
    HashTable* table = create_table();
    char search_target[64] = {0};

    for (i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--search") == 0 && i + 1 < argc) {
            strncpy(search_target, argv[i + 1], sizeof(search_target) - 1);
        }
    }

    if (argc > 1 && strcmp(argv[1], "--demo") == 0) {
        hash_insert(table, 1, "E101", "Accident_Site_Photo.jpg", "Image Evidence", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "2026-11-20");
        hash_insert(table, 2, "E102", "Forensic_Autopsy_Report.pdf", "Document Evidence", "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8", "2026-11-21");
        hash_insert(table, 3, "E103", "CCTV_Surveillance_Footage.mp4", "Video Evidence", "4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a", "2026-11-21");
        strcpy(search_target, "E101");
    } else {
        char line[1024];
        while (fgets(line, sizeof(line), stdin)) {
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

            hash_insert(table, id, code, title, category, hash, date);
        }
    }

    printf("{\n");
    printf("  \"algorithm\": \"Hash Table (Separate Chaining)\",\n");
    printf("  \"table_size\": %d,\n", TABLE_SIZE);
    printf("  \"total_entries\": %d,\n", table->total_entries);
    printf("  \"collisions\": %d,\n", table->collisions);

    if (strlen(search_target) > 0) {
        int bucket = 0, comps = 0;
        HashNode* found = hash_search(table, search_target, &bucket, &comps);
        printf("  \"search\": {\n");
        printf("    \"target\": \"%s\",\n", search_target);
        printf("    \"bucket\": %d,\n", bucket);
        printf("    \"comparisons\": %d,\n", comps);
        printf("    \"found\": %s,\n", found ? "true" : "false");
        if (found) {
            printf("    \"item\": {\n");
            printf("      \"id\": %d,\n", found->id);
            printf("      \"code\": \"%s\",\n", found->code);
            printf("      \"title\": \"%s\",\n", found->title);
            printf("      \"category\": \"%s\"\n", found->category);
            printf("    }\n");
        } else {
            printf("    \"item\": null\n");
        }
        printf("  },\n");
    }

    printf("  \"buckets\": [\n");
    int first_bucket = 1;
    for (i = 0; i < TABLE_SIZE; i++) {
        if (table->buckets[i]) {
            if (!first_bucket) printf(",\n");
            first_bucket = 0;
            printf("    {\n      \"index\": %d,\n      \"chain\": [", i);
            HashNode* n = table->buckets[i];
            while (n) {
                printf("\"%s\"", n->code);
                if (n->next) printf(", ");
                n = n->next;
            }
            printf("]\n    }");
        }
    }
    printf("\n  ]\n}\n");

    return 0;
}
