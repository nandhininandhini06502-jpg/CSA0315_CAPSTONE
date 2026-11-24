/*
 * DIGITAL EVIDENCE SYSTEM - Queue Algorithm (FIFO)
 * File: queue.c
 * Purpose: First-In-First-Out queue to manage pending digital evidence verification requests.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_STR 256

typedef struct QueueNode {
    int id;
    char code[32];
    char title[MAX_STR];
    char category[MAX_STR];
    char upload_time[64];
    struct QueueNode* next;
} QueueNode;

typedef struct {
    QueueNode* front;
    QueueNode* rear;
    int size;
} VerificationQueue;

VerificationQueue* create_queue() {
    VerificationQueue* q = (VerificationQueue*)malloc(sizeof(VerificationQueue));
    q->front = q->rear = NULL;
    q->size = 0;
    return q;
}

void enqueue(VerificationQueue* q, int id, const char* code, const char* title, const char* category, const char* upload_time) {
    QueueNode* node = (QueueNode*)malloc(sizeof(QueueNode));
    node->id = id;
    strncpy(node->code, code, sizeof(node->code) - 1);
    node->code[sizeof(node->code) - 1] = '\0';
    strncpy(node->title, title, sizeof(node->title) - 1);
    node->title[sizeof(node->title) - 1] = '\0';
    strncpy(node->category, category, sizeof(node->category) - 1);
    node->category[sizeof(node->category) - 1] = '\0';
    strncpy(node->upload_time, upload_time, sizeof(node->upload_time) - 1);
    node->upload_time[sizeof(node->upload_time) - 1] = '\0';
    node->next = NULL;

    if (q->rear == NULL) {
        q->front = q->rear = node;
    } else {
        q->rear->next = node;
        q->rear = node;
    }
    q->size++;
}

QueueNode* dequeue(VerificationQueue* q) {
    QueueNode* temp;
    if (q->front == NULL) return NULL;
    temp = q->front;
    q->front = q->front->next;
    if (q->front == NULL) q->rear = NULL;
    q->size--;
    return temp;
}

int main(int argc, char* argv[]) {
    int i;
    VerificationQueue* q = create_queue();
    int do_dequeue = 0;

    for (i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--dequeue") == 0) {
            do_dequeue = 1;
        }
    }

    if (argc > 1 && strcmp(argv[1], "--demo") == 0) {
        enqueue(q, 101, "E101", "Accident_Site_Photo.jpg", "Image Evidence", "10:30:00");
        enqueue(q, 102, "E102", "Forensic_Autopsy_Report.pdf", "Document Evidence", "11:15:20");
        enqueue(q, 103, "E103", "CCTV_Surveillance_Footage.mp4", "Video Evidence", "12:05:40");
    } else {
        char line[1024];
        while (fgets(line, sizeof(line), stdin)) {
            if (line[0] == '\n' || line[0] == '\r') continue;
            int id;
            char code[32] = {0}, title[MAX_STR] = {0}, category[MAX_STR] = {0}, time[64] = {0};
            char* token = strtok(line, "|\n\r");
            if (!token) continue;
            id = atoi(token);

            token = strtok(NULL, "|\n\r");
            if (token) strncpy(code, token, sizeof(code) - 1);

            token = strtok(NULL, "|\n\r");
            if (token) strncpy(title, token, sizeof(title) - 1);

            token = strtok(NULL, "|\n\r");
            if (token) strncpy(category, token, sizeof(category) - 1);

            token = strtok(NULL, "|\n\r"); // skip hash if passed
            token = strtok(NULL, "|\n\r");
            if (token) strncpy(time, token, sizeof(time) - 1);

            enqueue(q, id, code, title, category, time);
        }
    }

    printf("{\n");
    printf("  \"algorithm\": \"FIFO Verification Queue\",\n");
    printf("  \"total_pending\": %d,\n", q->size);

    if (do_dequeue && q->size > 0) {
        QueueNode* popped = dequeue(q);
        printf("  \"dequeued\": {\"id\": %d, \"code\": \"%s\", \"title\": \"%s\"},\n", popped->id, popped->code, popped->title);
        free(popped);
    } else {
        printf("  \"dequeued\": null,\n");
    }

    printf("  \"queue_order\": [\n");
    QueueNode* curr = q->front;
    int idx = 1;
    while (curr) {
        printf("    {\"position\": %d, \"id\": %d, \"code\": \"%s\", \"title\": \"%s\", \"time\": \"%s\"}%s\n",
               idx++, curr->id, curr->code, curr->title, curr->upload_time, curr->next ? "," : "");
        curr = curr->next;
    }
    printf("  ]\n}\n");

    return 0;
}
