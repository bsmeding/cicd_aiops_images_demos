// Jenkins declarative pipeline demo
// Uses bsmeding/aiops_cicd_ubuntu:latest as the build container.
// Scheduled weekly via a Jenkins cron trigger.

pipeline {
    agent {
        docker {
            image 'bsmeding/aiops_cicd_ubuntu:latest'
            args '--entrypoint=""'
        }
    }

    triggers {
        cron('H 8 * * 1')   // Every Monday around 08:00
    }

    environment {
        OPENAI_API_KEY    = credentials('openai-api-key')
        ANTHROPIC_API_KEY = credentials('anthropic-api-key')
    }

    stages {
        stage('Lint') {
            steps {
                sh 'ruff check .'
                sh 'mypy src tests --ignore-missing-imports'
            }
        }

        stage('Schema Contracts') {
            steps {
                sh 'python tools/validate_json_schemas.py schemas/'
                sh 'pytest tests/contracts -vv'
            }
        }

        stage('Incident Replay') {
            steps {
                sh '''
                    python replay/run_replay.py replay/incidents/*.jsonl \
                        --output build/replay-results.json
                    python replay/check_regressions.py build/replay-results.json
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'build/replay-results.json', allowEmptyArchive: true
                }
            }
        }

        stage('Prompt Tests') {
            steps {
                sh 'pytest tests/prompts -vv --junitxml=prompt-results.xml'
            }
            post {
                always {
                    junit 'prompt-results.xml'
                }
            }
        }

        stage('Agent Tests') {
            steps {
                sh 'pytest tests/agents -vv --junitxml=agent-results.xml'
            }
            post {
                always {
                    junit 'agent-results.xml'
                }
            }
        }

        stage('RAG Evaluation') {
            steps {
                sh 'python rag/build_index.py --source docs/runbooks --output build/index'
                sh '''
                    python eval/run_ragas.py \
                        --dataset eval/datasets/network_runbooks.jsonl \
                        --output build/ragas-report.json
                '''
                sh 'pytest tests/rag -vv --junitxml=rag-results.xml'
            }
            post {
                always {
                    junit 'rag-results.xml'
                    archiveArtifacts artifacts: 'build/ragas-report.json', allowEmptyArchive: true
                }
            }
        }

        stage('LLM Smoke') {
            steps {
                sh 'python tools/llm_smoke.py'
            }
        }
    }

    post {
        failure {
            echo 'Pipeline failed — check artifacts for details.'
        }
        success {
            echo 'All AIOps CI/CD demo stages passed.'
        }
    }
}
