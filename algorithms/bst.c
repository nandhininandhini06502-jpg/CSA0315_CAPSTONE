/*
 * DIGITAL EVIDENCE SYSTEM - Binary Search Tree (BST) Algorithm
 * File: bst.c
 * Purpose: Organizes digital evidence hierarchically by Evidence ID.
 * Supports Insertion, Inorder Traversal, Preorder Traversal, and Search.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_STR 256

typedef struct BSTNode {
    int id;
    char code[32];
    char title[MAX_STR];
    char category[MAX_STR];
    char hash[128];
    char date[64];
    struct BSTNode* left;
    struct BSTNode* right;
} BSTNode;

BSTNode* create_node(int id, const char* code, const char* title, const char* category, const char* hash, const char* date) {
    BSTNode* node = (BSTNode*)malloc(sizeof(BSTNode));
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
    node->left = NULL;
    node->right = NULL;
    return node;
}

BSTNode* bst_insert(BSTNode* root, int id, const char* code, const char* title, const char* category, const char* hash, const char* date) {
    if (root == NULL) {
        return create_node(id, code, title, category, hash, date);
    }
    if (id < root->id) {
        root->left = bst_insert(root->left, id, code, title, category, hash, date);
    } else if (id > root->id) {
        root->right = bst_insert(root->right, id, code, title, category, hash, date);
    }
    return root;
}

BSTNode* bst_search(BSTNode* root, int id, int* steps) {
    if (root == NULL) return NULL;
    (*steps)++;
    if (root->id == id) return root;
    if (id < root->id) return bst_search(root->left, id, steps);
    return bst_search(root->right, id, steps);
}

int first_inorder = 1;
void print_inorder(BSTNode* root) {
    if (root == NULL) return;
    print_inorder(root->left);
    if (!first_inorder) printf(", ");
    first_inorder = 0;
    printf("{\"id\": %d, \"code\": \"%s\", \"title\": \"%s\"}", root->id, root->code, root->title);
    print_inorder(root->right);
}

int first_preorder = 1;
void print_preorder(BSTNode* root) {
    if (root == NULL) return;
    if (!first_preorder) printf(", ");
    first_preorder = 0;
    printf("{\"id\": %d, \"code\": \"%s\", \"title\": \"%s\"}", root->id, root->code, root->title);
    print_preorder(root->left);
    print_preorder(root->right);
}

int bst_height(BSTNode* root) {
    if (root == NULL) return 0;
    int lh = bst_height(root->left);
    int rh = bst_height(root->right);
    return 1 + (lh > rh ? lh : rh);
}

int main(int argc, char* argv[]) {
    int i;
    BSTNode* root = NULL;
    int search_id = -1;

    for (i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--search") == 0 && i + 1 < argc) {
            search_id = atoi(argv[i + 1]);
        }
    }

    if (argc > 1 && strcmp(argv[1], "--demo") == 0) {
        root = bst_insert(root, 102, "E102", "Forensic_Autopsy_Report.pdf", "Document Evidence", "hash2", "2026-11-21");
        root = bst_insert(root, 101, "E101", "Accident_Site_Photo.jpg", "Image Evidence", "hash1", "2026-11-20");
        root = bst_insert(root, 104, "E104", "Voice_Call_Recording.mp3", "Audio Evidence", "hash4", "2026-11-21");
        root = bst_insert(root, 103, "E103", "CCTV_Surveillance_Footage.mp4", "Video Evidence", "hash3", "2026-11-21");
        search_id = 103;
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

            root = bst_insert(root, id, code, title, category, hash, date);
        }
    }

    printf("{\n");
    printf("  \"algorithm\": \"Binary Search Tree\",\n");
    printf("  \"tree_height\": %d,\n", bst_height(root));
    printf("  \"root_id\": %d,\n", root ? root->id : 0);

    if (search_id != -1) {
        int steps = 0;
        BSTNode* found = bst_search(root, search_id, &steps);
        printf("  \"search\": {\n");
        printf("    \"target_id\": %d,\n", search_id);
        printf("    \"steps\": %d,\n", steps);
        printf("    \"found\": %s,\n", found ? "true" : "false");
        if (found) {
            printf("    \"item\": {\"id\": %d, \"code\": \"%s\", \"title\": \"%s\"}\n", found->id, found->code, found->title);
        } else {
            printf("    \"item\": null\n");
        }
        printf("  },\n");
    }

    printf("  \"inorder_traversal\": [");
    first_inorder = 1;
    print_inorder(root);
    printf("],\n");

    printf("  \"preorder_traversal\": [");
    first_preorder = 1;
    print_preorder(root);
    printf("]\n");
    printf("}\n");

    return 0;
}
