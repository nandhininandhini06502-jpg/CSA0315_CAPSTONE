/*
 * DIGITAL EVIDENCE SYSTEM - Linked List Algorithm
 * File: linkedlist.c
 * Purpose: Organizes digital evidence records in a dynamic singly linked list.
 * Supports Insertion, Traversal, Deletion, and JSON output for Django integration.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_STR 256

typedef struct EvidenceNode {
    int id;
    char code[32];
    char title[MAX_STR];
    char category[MAX_STR];
    char hash[128];
    char date[64];
    struct EvidenceNode* next;
} EvidenceNode;

EvidenceNode* head = NULL;

EvidenceNode* create_node(int id, const char* code, const char* title, const char* category, const char* hash, const char* date) {
    EvidenceNode* node = (EvidenceNode*)malloc(sizeof(EvidenceNode));
    if (!node) return NULL;
    node->id = id;
    strncpy(node->code, code, sizeof(node->code) - 1);
    node->code[sizeof(node->code) - 1] = '\0';
    strncpy(node->title, title, sizeof(node->title) - 1);
    node->title[sizeof(node->title) - 1] = '\0';
    strncpy(node->category, category, sizeof(node->category) - 1);
    node->category[sizeof(node->category) - 1] = '\0';
    strncpy(node->hash, hash, sizeof(node->hash) - 1);
    node->hash[sizeof(node->hash) - 1] = '\0';
    strncpy(node->date, date, sizeof(node->date) - 1);
    node->date[sizeof(node->date) - 1] = '\0';
    node->next = NULL;
    return node;
}

void insert_evidence(int id, const char* code, const char* title, const char* category, const char* hash, const char* date) {
    EvidenceNode* new_node = create_node(id, code, title, category, hash, date);
    if (!new_node) return;

    if (head == NULL) {
        head = new_node;
        return;
    }

    EvidenceNode* temp = head;
    while (temp->next != NULL) {
        temp = temp->next;
    }
    temp->next = new_node;
}

int delete_evidence(int id) {
    EvidenceNode *temp = head, *prev = NULL;

    if (temp != NULL && temp->id == id) {
        head = temp->next;
        free(temp);
        return 1;
    }

    while (temp != NULL && temp->id != id) {
        prev = temp;
        temp = temp->next;
    }

    if (temp == NULL) return 0;

    prev->next = temp->next;
    free(temp);
    return 1;
}

void print_json() {
    printf("{\n  \"algorithm\": \"Singly Linked List\",\n  \"count\": ");
    int count = 0;
    EvidenceNode* curr = head;
    while (curr) { count++; curr = curr->next; }
    printf("%d,\n  \"nodes\": [\n", count);

    curr = head;
    while (curr) {
        printf("    {\n");
        printf("      \"id\": %d,\n", curr->id);
        printf("      \"code\": \"%s\",\n", curr->code);
        printf("      \"title\": \"%s\",\n", curr->title);
        printf("      \"category\": \"%s\",\n", curr->category);
        printf("      \"hash\": \"%s\",\n", curr->hash);
        printf("      \"date\": \"%s\",\n", curr->date);
        printf("      \"next_id\": %s\n", curr->next ? "true" : "false");
        printf("    }%s\n", curr->next ? "," : "");
        curr = curr->next;
    }
    printf("  ]\n}\n");
}

int main(int argc, char* argv[]) {
    // If run with sample demo argument
    if (argc > 1 && strcmp(argv[1], "--demo") == 0) {
        printf("--- Linked List Algorithm Demo ---\n");
        insert_evidence(1, "E101", "Accident_Site_Photo.jpg", "Image Evidence", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "2026-11-20");
        insert_evidence(2, "E102", "Forensic_Autopsy_Report.pdf", "Document Evidence", "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8", "2026-11-21");
        insert_evidence(3, "E103", "CCTV_Surveillance_Footage.mp4", "Video Evidence", "4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a", "2026-11-21");
        print_json();
        return 0;
    }

    // Read evidence records from standard input:
    // Format per line: ID|CODE|TITLE|CATEGORY|HASH|DATE
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

        insert_evidence(id, code, title, category, hash, date);
    }

    print_json();
    return 0;
}
